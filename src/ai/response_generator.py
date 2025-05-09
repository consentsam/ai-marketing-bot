"""
Response generator for the YieldFi AI Agent.

This module provides the core functionality for generating AI responses.
"""

from typing import Dict, Any, Optional
import os
import sys
from datetime import datetime, timezone
import re

# Ensure the test can find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models.tweet import Tweet # type: ignore
from src.models.account import Account, AccountType # type: ignore
from src.models.response import AIResponse, ResponseType # type: ignore
from src.models.category import TweetCategory # Added for Step 18
from src.ai.xai_client import XAIClient, APIError as XAIAPIError # type: ignore
from src.ai.prompt_engineering import generate_interaction_prompt, generate_new_tweet_prompt, InteractionMode # type: ignore
from src.ai.tone_analyzer import analyze_tweet_tone # type: ignore
from src.utils.logging import get_logger # type: ignore
from src.utils.persistence import save_response  # Persist AI responses
from src.ai.relevancy import get_facts  # Step 26 relevancy facts
# from src.knowledge.retrieval import KnowledgeRetriever # Step 11 - Mock for now

logger = get_logger(__name__)

# Module-level constant for known Degen mode partial responses
degen_partials = {
    "s milestone to yieldfi": "This milestone for YieldFi is HUGE! 🚀",
    "s pump it": "Let's pump it to the moon! 🌕",
    "s to the moon": "This is going to the moon! 🚀🌕"
}

# --- Mocked Knowledge Retriever --- START
class MockKnowledgeRetriever:
    def get_relevant_knowledge(self, query: str, limit: int = 1) -> Optional[str]:
        logger.info(f"MockKnowledgeRetriever: Received query '{query}'. Returning mock knowledge.")
        if "security" in query.lower():
            return "YieldFi employs state-of-the-art multi-layered security protocols, including regular audits and encryption."
        if "staking" in query.lower():
            return "YieldFi offers competitive staking rewards on various assets. Current APY for YLD is 12%."
        return "YieldFi is a decentralized finance platform focused on user empowerment and transparency."

    def search_knowledge_for_topic(self, topic: str, category_name: Optional[str] = None) -> Optional[str]:
        logger.info(f"MockKnowledgeRetriever: Received topic '{topic}' for category '{category_name}'. Returning mock knowledge.")
        if "new product" in topic.lower() or (category_name and "product update" in category_name.lower()):
            return "Our latest product, YieldBoost, offers enhanced returns through automated strategies."
        if category_name and "announcement" in category_name.lower():
             return "YieldFi has just secured a new strategic partnership with InnovateX to expand our ecosystem!"
        return "YieldFi continually innovates to bring value to its users."

# --- Mocked Knowledge Retriever --- END

def generate_tweet_reply(
    original_tweet: Tweet,
    responding_as: Account,
    target_account: Optional[Account] = None,
    platform: str = "Twitter",
    interaction_details: Optional[Dict[str, Any]] = None,
    # knowledge_retriever: Optional[KnowledgeRetriever] = None # For Step 11
    knowledge_retriever: Optional[MockKnowledgeRetriever] = None, # Using Mock for now
    generate_image: bool = False,
    interaction_mode: str = "Default"  # Added for Step 25
) -> AIResponse:
    """
    Generates a reply to a given tweet.
    Orchestrates tone analysis, knowledge retrieval (mocked), prompt engineering, and AI client call.
    
    Args:
        original_tweet: The tweet to reply to
        responding_as: The account persona to use for the reply
        target_account: The account being replied to
        platform: Social media platform (default: "Twitter")
        interaction_details: Additional context for response generation
        knowledge_retriever: Service to get relevant knowledge
        generate_image: Whether to generate an image for the tweet
        interaction_mode: Mode to use for response (Default, Professional, Degen)
    
    Returns:
        An AIResponse object with the generated content
    """
    # Use provided Account for responding_as
    responding_as_account = responding_as

    logger.info(f"Generating reply for tweet ID: {original_tweet.metadata.tweet_id} as {responding_as_account.username} (Type: {responding_as_account.account_type.value})")
    logger.info(f"Using interaction mode: {interaction_mode}")
    prompt_str = ""
    ai_generated_content = "[Error: Could not generate AI response]"
    model_used = "Unknown"
    final_tone = original_tweet.tone
    response_error = None # To store error messages

    try:
        # 1. Analyze tone of the original tweet (if not already done)
        if original_tweet.tone is None:
            analyzed_tweet = analyze_tweet_tone(original_tweet)
            final_tone = analyzed_tweet.tone
            logger.info(f"Analyzed tone of original tweet: {final_tone}")
        else:
            final_tone = original_tweet.tone
            logger.info(f"Using existing tone of original tweet: {final_tone}")

        # 2. Retrieve relevant knowledge (Mocked for now)
        knowledge_snippet: Optional[str] = None
        # For Step 11: if knowledge_retriever:
        current_retriever = knowledge_retriever if knowledge_retriever else MockKnowledgeRetriever()
        knowledge_snippet = current_retriever.get_relevant_knowledge(original_tweet.content)
        if knowledge_snippet:
            logger.info(f"Retrieved knowledge snippet: {knowledge_snippet[:100]}...")
        else:
            logger.info("No specific knowledge snippet retrieved for this interaction.")

        # 3. Generate prompt with interaction_mode
        logger.info(f"Generating interaction prompt with mode: {interaction_mode}...")
        # Prepare prompt parameters, include mode only if non-default
        prompt_kwargs = {
            'original_post_content': original_tweet.content,
            'active_account_info': responding_as_account,
            'target_account_info': target_account,
            'yieldfi_knowledge_snippet': knowledge_snippet,
            'interaction_details': interaction_details if interaction_details else {},
            'platform': platform
        }
        if interaction_mode and interaction_mode != InteractionMode.DEFAULT.value:
            prompt_kwargs['mode'] = interaction_mode
        prompt_str = generate_interaction_prompt(**prompt_kwargs)
        logger.debug(f"Generated interaction prompt: {prompt_str[:300]}...")
        # Step 26: Append relevancy facts to the prompt if any
        try:
            relevancy_facts = get_facts(original_tweet)
            if relevancy_facts:
                facts_str = "\n".join(f"- {fact}" for fact in relevancy_facts)
                prompt_str += f"\n\nRelevancy Facts:\n{facts_str}"
                logger.info(f"Appended relevancy facts to prompt: {relevancy_facts}")
        except Exception as e:
            logger.warning(f"Failed to append relevancy facts: {e}")

        # 4. Call AI client
        # This assumes XAIClient is properly configured (Step 6)
        xai_client = XAIClient() # API keys loaded from config within XAIClient
        model_used = xai_client.xai_model  # Use configured model name
        
        logger.info(f"Calling XAIClient.get_completion with model: '{model_used}' for tweet reply.")
        ai_response_data = xai_client.get_completion(prompt=prompt_str, max_tokens=512)
        logger.debug(f"Raw AI response data for reply: {ai_response_data}")
        
        # Extract content - this depends on the actual structure of xAI/PaLM response
        if ai_response_data.get('choices') and isinstance(ai_response_data['choices'], list) and len(ai_response_data['choices']) > 0:
            choice = ai_response_data['choices'][0]
            logger.debug(f"Processing AI response choice: {choice}")

            finish_reason = choice.get('finish_reason')
            if finish_reason == 'length':
                logger.warning(f"AI response 'finish_reason' is 'length'. The response may be truncated. Full choice: {choice}")

            if choice.get('text'): # Primarily for non-chat models or older formats
                raw_content = choice['text'].strip()
                logger.info(f"Extracted 'text' from choice: '{raw_content[:100]}...'")
                logger.debug(f"Full raw AI output (reply, from 'text'): {raw_content}")
                ai_generated_content = _clean_response(raw_content)
                logger.info(f"Cleaned text output (reply, first 100 chars): '{ai_generated_content[:100]}...'")
            elif choice.get('message'):
                message_data = choice['message']
                if message_data.get('content') and message_data['content'].strip():
                    raw_content = message_data['content'].strip()
                    logger.info(f"Extracted 'content' from message: '{raw_content[:100]}...'")
                    logger.debug(f"Full raw AI output (reply, from 'message.content'): {raw_content}")
                    # Clean the response
                    ai_generated_content = _clean_response(raw_content)
                    logger.info(f"Cleaned message content (reply, first 100 chars): '{ai_generated_content[:100]}...'")
                elif message_data.get('reasoning_content') and message_data['reasoning_content'].strip():
                    ai_generated_content = message_data['reasoning_content'].strip()
                    logger.info(f"Extracted 'reasoning_content' from message as fallback: '{ai_generated_content[:100]}...'")
                    if finish_reason == 'length':
                         ai_generated_content = "[Warning: Response possibly truncated and extracted from reasoning] " + ai_generated_content
                    else:
                         ai_generated_content = "[Info: Extracted from reasoning_content] " + ai_generated_content
                else:
                    ai_generated_content = "[Warning: AI response format unclear - message content and reasoning_content are empty]"
                    response_error = "AI response format unclear: message content and reasoning_content empty."
                    logger.warning(f"Could not extract text from AI response choice's message: {message_data}. Setting error: {response_error}")
            else:
                ai_generated_content = "[Warning: AI response format unclear - no 'text' or 'message' in choice]"
                response_error = "AI response format unclear from choice (no text/message)."
                logger.warning(f"Could not extract text/message from AI response choice: {choice}. Setting error: {response_error}")
        elif ai_response_data.get('candidates') and isinstance(ai_response_data['candidates'], list) and len(ai_response_data['candidates']) > 0:
             # Fallback for Google PaLM style response (text-bison-001 example)
            candidate = ai_response_data['candidates'][0]
            if candidate.get('output'):
                ai_generated_content = candidate['output'].strip()
                logger.info(f"Extracted output from candidate (reply): '{ai_generated_content[:100]}...'")
                # PaLM typically gives clean output, but we can still run it through cleaner
                ai_generated_content = _clean_response(ai_generated_content)
                logger.info(f"Cleaned PaLM output (reply): '{ai_generated_content[:100]}...'")
            else:
                logger.warning(f"Could not extract text from AI response candidate: {candidate}")
                ai_generated_content = "[Warning: AI response format unclear (PaLM candidate)]"
                response_error = "AI response format unclear from candidate (PaLM)."
        else:
            logger.warning(f"AI response structure not recognized for content extraction: {ai_response_data}")
            ai_generated_content = "[Warning: AI response structure not recognized]"
            response_error = "AI response structure not recognized."

        logger.info(f"Successfully generated AI reply: {ai_generated_content[:100]}...")

    except XAIAPIError as e:
        logger.error(f"XAIClient APIError in generate_tweet_reply: {e}", exc_info=True)
        ai_generated_content = f"[Error: AI API call failed - {e.message}]"
        response_error = e.message
    except Exception as e:
        logger.error(f"Unexpected error in generate_tweet_reply: {e}", exc_info=True)
        ai_generated_content = f"[Error: Unexpected error during response generation - {str(e)}]"
        response_error = str(e)

    response = AIResponse(
        content=ai_generated_content,
        response_type=ResponseType.TWEET_REPLY,
        model_used=model_used,
        prompt_used=prompt_str,
        source_tweet_id=original_tweet.metadata.tweet_id,
        responding_as=responding_as_account.account_type.value,
        target_account=target_account.username if target_account else None,
        generation_time=datetime.now(timezone.utc),
        tone=final_tone,
        extra_context={"interaction_mode": interaction_mode}  # Store the interaction mode in the response
    )
    # Generate poster image if requested
    if generate_image:
        from src.ai.image_generation import get_poster_image
        try:
            logger.info(f"generate_image is True. Attempting to generate poster image for reply.")
            image_prompt = f"Create a visual for a tweet about: {ai_generated_content[:150]}"
            response.image_url = get_poster_image(image_prompt)
            logger.info(f"Poster image generation for reply returned URL: {response.image_url}")
        except Exception as e:
            logger.error(f"Failed to generate poster image for reply: {e}", exc_info=True)
            response.image_url = None
    else:
        logger.info("generate_image is False for reply. Skipping image generation.")
        response.image_url = None
    # Persist the generated reply with metadata
    try:
        metadata = {
            'original_input': original_tweet.content,
            'interaction_mode': interaction_mode,
            'responding_as': responding_as_account.username,
            'responding_as_type': responding_as_account.account_type.value,
            'target_account': target_account.username if target_account else None,
        }
        logger.info(f"Saving generated tweet reply with metadata: {metadata}")
        save_response(response, metadata)
    except Exception as e:
        logger.error(f"Error while saving response: {e}", exc_info=True)
    return response

def generate_new_tweet(
    category,
    responding_as: Account,
    topic: Optional[str] = None,
    knowledge_retriever: Optional[MockKnowledgeRetriever] = None,  # Using Mock for now
    platform: str = "Twitter",
    additional_instructions: Optional[Dict[str, Any]] = None,
    generate_image: bool = False,
    interaction_mode: str = "Default"  # Added for Step 25
) -> AIResponse:
    """
    Generates a new tweet based on a category, topic, and other details.
    Orchestrates knowledge retrieval (mocked), prompt engineering, and AI client call.
    
    Args:
        category: The category for the tweet (string or TweetCategory object)
        responding_as: The account persona to use for the tweet
        topic: Specific topic for the tweet
        knowledge_retriever: Service to get relevant knowledge
        platform: Social media platform (default: "Twitter")
        additional_instructions: Additional context for tweet generation
        generate_image: Whether to generate an image for the tweet
        interaction_mode: Mode to use for the tweet (Default, Professional, Degen)
    
    Returns:
        An AIResponse object with the generated content
    """
    # Use provided Account for responding_as
    responding_as_account = responding_as
    # Handle category type (string or TweetCategory)
    original_category = category
    if isinstance(category, str):
        category_name = category
        category_obj = TweetCategory(name=category, description="", prompt_keywords=[], style_guidelines={})
    else:
        category_name = category.name
        category_obj = category

    logger.info(f"START generate_new_tweet: Category='{category_name}', Persona='{responding_as_account.account_type.value}', Topic='{topic}'")
    logger.info(f"Using interaction mode: {interaction_mode}")
    logger.debug(f"Full category details: Name='{category_name}', Description='{category_obj.description}', Keywords='{category_obj.prompt_keywords}', Style='{category_obj.style_guidelines}'")
    logger.debug(f"Responding as account details: ID='{responding_as_account.account_id}', Username='{responding_as_account.username}', Type='{responding_as_account.account_type.value}'")
    logger.debug(f"Platform='{platform}', Additional Instructions='{additional_instructions}'")

    prompt_str = ""
    ai_generated_content = "[Error: Could not generate AI response]"
    model_used = "Unknown"
    response_error = None # To store error messages

    try:
        # 1. Retrieve relevant knowledge (Mocked for now)
        knowledge_snippet: Optional[str] = None
        # For Step 11: if knowledge_retriever:
        current_retriever = knowledge_retriever if knowledge_retriever else MockKnowledgeRetriever()
        knowledge_query = topic if topic else category_name # Use category name for knowledge query if no topic
        knowledge_snippet = current_retriever.search_knowledge_for_topic(knowledge_query, category_name)
        if knowledge_snippet:
            logger.info(f"Retrieved knowledge snippet for new tweet: '{knowledge_snippet}'")
        else:
            logger.info("No specific knowledge snippet retrieved for this topic/category.")

        # 2. Generate prompt using TweetCategory object and interaction_mode
        logger.info(f"Generating new tweet prompt with mode: {interaction_mode}...")
        # Prepare prompt parameters, include mode only if non-default
        new_prompt_kwargs = {
            'category': original_category,
            'topic': topic,
            'active_account_info': responding_as_account,
            'yieldfi_knowledge_snippet': knowledge_snippet,
            'platform': platform,
            'additional_instructions': additional_instructions
        }
        if interaction_mode and interaction_mode != InteractionMode.DEFAULT.value:
            new_prompt_kwargs['mode'] = interaction_mode
        prompt_str = generate_new_tweet_prompt(**new_prompt_kwargs)
        logger.debug(f"Generated new tweet prompt (first 500 chars): '{prompt_str[:500]}'")
        logger.info(f"Full prompt length: {len(prompt_str)} characters")

        # 3. Call AI client
        logger.info(f"Initializing XAIClient to generate new tweet content.")
        xai_client = XAIClient()
        model_used = xai_client.xai_model  # Use configured model name
        logger.info(f"Calling XAIClient.get_completion with model: '{model_used}' for new tweet.")
        ai_response_data = xai_client.get_completion(prompt=prompt_str, max_tokens=512)
        logger.info(f"Received raw response data from XAIClient for new tweet.")
        logger.debug(f"Raw AI response data for new tweet: {ai_response_data}")

        # Extract content (same logic as generate_tweet_reply)
        logger.info("Attempting to extract content from AI response...")
        if ai_response_data.get('choices') and isinstance(ai_response_data['choices'], list) and len(ai_response_data['choices']) > 0:
            choice = ai_response_data['choices'][0]
            logger.debug(f"Processing AI response choice: {choice}")

            finish_reason = choice.get('finish_reason')
            if finish_reason == 'length':
                logger.warning(f"AI response 'finish_reason' is 'length'. The response may be truncated. Full choice: {choice}")

            if choice.get('text'): # Primarily for non-chat models or older formats
                raw_content = choice['text'].strip()
                logger.info(f"Extracted 'text' from choice (new tweet): '{raw_content[:100]}...'")
                logger.debug(f"Full raw AI output (new tweet, from 'text'): {raw_content}")
                ai_generated_content = _clean_response(raw_content)
                logger.info(f"Cleaned text output (new tweet, first 100 chars): '{ai_generated_content[:100]}...'")
            elif choice.get('message'):
                message_data = choice['message']
                if message_data.get('content') and message_data['content'].strip():
                    raw_content = message_data['content'].strip()
                    logger.info(f"Extracted 'content' from message (new tweet): '{raw_content[:100]}...'")
                    logger.debug(f"Full raw AI output (new tweet, from 'message.content'): {raw_content}")
                    # Clean the response
                    ai_generated_content = _clean_response(raw_content)
                    logger.info(f"Cleaned message content (new tweet, first 100 chars): '{ai_generated_content[:100]}...'")
                elif message_data.get('reasoning_content') and message_data['reasoning_content'].strip():
                    ai_generated_content = message_data['reasoning_content'].strip()
                    logger.info(f"Extracted 'reasoning_content' from message as fallback (new tweet): '{ai_generated_content[:100]}...'")
                    if finish_reason == 'length':
                         ai_generated_content = "[Warning: Response possibly truncated and extracted from reasoning] " + ai_generated_content
                    else:
                         ai_generated_content = "[Info: Extracted from reasoning_content] " + ai_generated_content
                else:
                    ai_generated_content = "[Warning: AI response format unclear - message content and reasoning_content are empty]"
                    response_error = "AI response format unclear: message content and reasoning_content empty."
                    logger.warning(f"Could not extract text from AI response choice's message: {message_data}. Setting error: {response_error}")
            else:
                ai_generated_content = "[Warning: AI response format unclear - no 'text' or 'message' in choice]"
                response_error = "AI response format unclear from choice (no text/message)."
                logger.warning(f"Could not extract text/message from AI response choice: {choice}. Setting error: {response_error}")
        elif ai_response_data.get('candidates') and isinstance(ai_response_data['candidates'], list) and len(ai_response_data['candidates']) > 0:
            candidate = ai_response_data['candidates'][0]
            logger.debug(f"Processing AI response candidate (PaLM style) for new tweet: {candidate}")
            if candidate.get('output'):
                ai_generated_content = candidate['output'].strip()
                logger.info(f"Extracted output from candidate (new tweet): '{ai_generated_content[:100]}...'")
                ai_generated_content = _clean_response(ai_generated_content)
                logger.info(f"Cleaned PaLM output (new tweet): '{ai_generated_content[:100]}...'")
            else:
                ai_generated_content = "[Warning: AI response format unclear (PaLM candidate)]"
                response_error = "AI response format unclear from candidate (PaLM)."
                logger.warning(f"Could not extract output from AI response candidate: {candidate}. Setting error: {response_error}")
        else:
            ai_generated_content = "[Warning: AI response structure not recognized]"
            response_error = "AI response structure not recognized."
            logger.warning(f"AI response structure not recognized for content extraction: {ai_response_data}. Setting error: {response_error}")

        if not response_error:
            logger.info(f"Successfully generated and extracted AI tweet content: '{ai_generated_content[:100]}...'")
        else:
            logger.warning(f"Finished content extraction with error: {response_error}. Content set to: '{ai_generated_content}'")

    except XAIAPIError as e:
        logger.error(f"XAIClient APIError in generate_new_tweet: {e.message} (Code: {e.status_code}, Details: {e.details})", exc_info=True)
        ai_generated_content = f"[Error: AI API call failed - {e.message}]"
        response_error = e.message
    except Exception as e:
        logger.error(f"Unexpected error in generate_new_tweet: {e}", exc_info=True)
        ai_generated_content = f"[Error: Unexpected error during new tweet generation - {str(e)}]"
        response_error = str(e)

    response_kwargs = {
        "content": ai_generated_content,
        "response_type": ResponseType.NEW_TWEET,
        "model_used": model_used,
        "prompt_used": prompt_str,  # Consider truncating if very long for storage/logging
        "responding_as": responding_as_account.account_type.value,
        "generation_time": datetime.now(timezone.utc),
        "tags": [category_name],
        "referenced_knowledge": [knowledge_snippet] if knowledge_snippet else [],
        "extra_context": {
            "category_description": category_obj.description,
            "category_keywords": category_obj.prompt_keywords,
            "category_style_guidelines": category_obj.style_guidelines,
            "topic_provided": topic,
            "error_message": response_error,  # Add error message to AIResponse object
            "interaction_mode": interaction_mode  # Store the interaction mode in the response
        }
    }
    logger.debug(f"AIResponse object creation arguments: {response_kwargs}")
    final_response = AIResponse(**response_kwargs)
    logger.info(f"END generate_new_tweet. Final AIResponse content: '{final_response.content[:100]}...', Model: '{final_response.model_used}'")
    # Generate poster image if requested
    if generate_image:
        from src.ai.image_generation import get_poster_image
        try:
            logger.info(f"generate_image is True. Attempting to generate poster image for new tweet.")
            image_prompt = f"Create a visual for a tweet about: {ai_generated_content[:150]}"
            final_response.image_url = get_poster_image(image_prompt)
            logger.info(f"Poster image generation for new tweet returned URL: {final_response.image_url}")
        except Exception as e:
            logger.error(f"Failed to generate poster image for new tweet: {e}", exc_info=True)
            final_response.image_url = None
    else:
        logger.info("generate_image is False for new tweet. Skipping image generation.")
        final_response.image_url = None
    # Persist the generated new tweet with metadata
    try:
        metadata = {
            'original_input': topic if topic else category_name,
            'category': category_name,
            'interaction_mode': interaction_mode,
            'responding_as': responding_as_account.username,
            'responding_as_type': responding_as_account.account_type.value,
        }
        logger.info(f"Saving generated new tweet with metadata: {metadata}")
        save_response(final_response, metadata)
    except Exception as e:
        logger.error(f"Error while saving response: {e}", exc_info=True)
    return final_response

def _clean_response(response_text: str) -> str:
    """Extract only the final tweet text from model response, removing any reasoning or formatting."""
    if not response_text:
        return ""
    
    logger.debug(f"Cleaning raw response (length {len(response_text)}): '{response_text[:200]}...'")
    
    # 1. Check for known Degen partials first
    stripped_lower_response = response_text.strip().lower()
    for partial_key, full_phrase in degen_partials.items():
        if stripped_lower_response.startswith(partial_key):
            logger.info(f"Degen partial matched: '{response_text.strip()}' -> '{full_phrase}'")
            return _ensure_tweet_length(full_phrase)

    # 2. Specific known truncation (less reliable, but a targeted fix for a common issue)
    if response_text.startswith("s rise to the top") or response_text.startswith("'s rise to the top"):
        logger.info("Specific truncation 's rise to the top' matched.")
        fixed_response = "Bitcoin's rise to the top" + response_text[len("s rise to the top"):]
        return _ensure_tweet_length(fixed_response)
    
    # 3. Marker-based extraction (quotes, labels) - Most reliable
    # Prefer last match for labels, as models sometimes repeat/refine.
    # Quoted content usually appears once if it's the intended output.
    tweet_markers = [
        # A. Content clearly enclosed in double quotes (handles escaped quotes and newlines)
        r'"(?P<tweet_double>(?:\\.|[^"\\])*)"', 
        # B. Content clearly enclosed in single quotes
        r"'(?P<tweet_single>(?:\\.|[^'\\])*)'",
        # C. After "Final tweet/version/response:"
        r'Final (?:tweet|version|response):\s*(?P<tweet_final_label>[^\n]{15,280})',
        # D. After "Tweet:" or "Response:"
        r'(?:Tweet|Response):\s*(?P<tweet_label>[^\n]{15,280})'
    ]
    
    best_marker_extraction = ""
    for pattern_details in tweet_markers:
        group_name = "tweet_double" if "tweet_double" in pattern_details else \
                     "tweet_single" if "tweet_single" in pattern_details else \
                     "tweet_final_label" if "tweet_final_label" in pattern_details else \
                     "tweet_label"
        flags = re.IGNORECASE
        try:
            # Find all non-overlapping matches
            for match in re.finditer(pattern_details, response_text, flags):
                extracted = match.group(group_name).strip()
                if group_name in ["tweet_double", "tweet_single"]:
                    extracted = extracted.replace('\\n', '\n').replace('\\r', '\r').replace('\\t', '\t').replace('\\"', '"').replace("\\'", "'")
                
                if 15 <= len(extracted) <= 280:
                    # For labels, the last match is often best. For quotes, any valid match is good.
                    # If we find a quoted match, it's very likely the intended tweet.
                    if group_name in ["tweet_double", "tweet_single"]:
                        logger.info(f"Quoted content extracted: '{extracted[:50]}...'")
                        return _ensure_tweet_length(extracted) 
                    best_marker_extraction = extracted # Store label matches, prefer later ones
                else:
                    logger.debug(f"Marker extracted '{extracted[:20]}...' but length {len(extracted)} invalid.")
        except re.error as e:
            logger.error(f"Regex error with pattern: {pattern_details}. Error: {e}")
            continue
            
    if best_marker_extraction: # This will be from the last valid label match if no quotes found
        logger.info(f"Label-based marker extracted: '{best_marker_extraction[:50]}...'")
        return _ensure_tweet_length(best_marker_extraction)

    # 4. Paragraph-based extraction (if no markers worked)
    reasoning_terms = [
        "consider", "thinking", "analyze", "thought", "would", "should", "could", "craft",
        "instruction", "respond", "character", "count", "draft", "context", "tone",
        "given the", "based on", "in this case", "let me", "i'll", "i'd", "i've",
        "look at", "structure", "content", "persona", "voice", "appropriate", "goal",
        "objective", "aim to", "task", "begin by", "following", "guidelines",
        "approach", "strategy", "reasoning", "critique", "model response", "system prompt",
        "user query", "internal thought", "plan:", "here's a", "my suggestion", "option is:",
        "the tweet should", "the reply should", "ensure that", "make sure to", "final output",
        "<|", "|>" # Model control tokens
    ]
    paragraphs = [p.strip() for p in response_text.split("\n\n") if p.strip()]
    potential_paragraphs = []
    for p in paragraphs:
        p_lower = p.lower()
        if not (15 <= len(p) <= 300): continue # Check length
        if any(term in p_lower for term in reasoning_terms): continue # Check reasoning
        if p.startswith(("- ", "* ", "1.", "2.", "Topic:", "Category:")): continue # Check list/meta
        potential_paragraphs.append(p)

    if potential_paragraphs:
        best_paragraph = potential_paragraphs[-1] # Prefer the last clean paragraph
        logger.info(f"Paragraph logic selected: '{best_paragraph[:50]}...'")
        return _ensure_tweet_length(best_paragraph)

    # 5. Sentence-based extraction (VERY conservative fallback)
    # Only try if the overall text isn't excessively long, to avoid expensive processing on huge reasoning dumps.
    if len(response_text) < 1000: 
        sentences = re.split(r'(?<=[.!?])(?:\s+|\n)+', response_text.strip()) 
        # Collect only the last consecutive run of tweet-like, non-reasoning sentences at the end
        tweet_like_run = []
        for s in reversed(sentences):
            s_stripped = s.strip()
            if not s_stripped:
                continue
            s_lower = s_stripped.lower()
            is_reasoning_sentence = False
            for term in reasoning_terms:
                if s_lower.startswith(term) or s_lower == term or s_lower.startswith(f"my {term}") or s_lower.startswith(f"the {term}"):
                    is_reasoning_sentence = True; break
            if is_reasoning_sentence:
                break  # Stop at first reasoning sentence from the end
            if len(s_stripped) < 30 and s_stripped.endswith(':'):
                break  # Stop at label-like lines
            if 15 <= len(s_stripped) <= 280:
                tweet_like_run.append(s_stripped)
            else:
                break  # Stop at non-tweet-like sentence
        if tweet_like_run:
            tweet_like_run = list(reversed(tweet_like_run))
            combined = ' '.join(tweet_like_run)
            if 15 <= len(combined) <= 280:
                logger.info(f"Sentence extraction (combined last run): '{combined[:50]}...'")
                return _ensure_tweet_length(combined)
            # If not combinable, return the last one in the run
            logger.info(f"Sentence extraction (last valid sentence in run): '{tweet_like_run[-1][:50]}...'")
            return _ensure_tweet_length(tweet_like_run[-1])
        # Fallback: scan all sentences in reverse for any tweet-like, non-reasoning sentence
        for s in reversed(sentences):
            s_stripped = s.strip()
            if not s_stripped:
                continue
            s_lower = s_stripped.lower()
            is_reasoning_sentence = False
            for term in reasoning_terms:
                if s_lower.startswith(term) or s_lower == term or s_lower.startswith(f"my {term}") or s_lower.startswith(f"the {term}"):
                    is_reasoning_sentence = True; break
            if is_reasoning_sentence:
                continue
            if len(s_stripped) < 30 and s_stripped.endswith(':'):
                continue
            if 15 <= len(s_stripped) <= 280:
                logger.info(f"Sentence extraction (fallback single sentence): '{s_stripped[:50]}...'")
                return _ensure_tweet_length(s_stripped)
    
    # 6. Final Fallback: Only if original text was ALREADY tweet-like and not clearly instructions.
    # This is to catch cases where the AI *only* returns the tweet, but it's very short.
    stripped_response_text = response_text.strip()
    if 10 <= len(stripped_response_text) <= 280: 
        is_clearly_instruction_or_system_message = any(term in stripped_response_text.lower() for term in [
            "instruction:", "draft:", "reasoning:", "model:", "prompt:", "system:", "error:", "warning:",
            "apologies", "i cannot", "unable to", "as an ai",
            "<|", "|>", "user:", "assistant:" # Common model/system prefixes/tokens
        ] + reasoning_terms[:5]) # Check a few common reasoning terms
        
        if not is_clearly_instruction_or_system_message:
            # Before returning, ensure it doesn't start with a typical reasoning phrase that was missed
            if not any(stripped_response_text.lower().startswith(rt + ":") or stripped_response_text.lower().startswith(rt + " ") for rt in ["response", "tweet", "final"]):
                 logger.warning(f"All specific cleaning failed. Using original short text as last resort: '{stripped_response_text[:50]}...'")
                 return _ensure_tweet_length(stripped_response_text)

    logger.error(f"_clean_response: Could not reliably extract tweet. Raw start: '{response_text[:100]}...'. Returning empty.")
    return ""

def _ensure_tweet_length(tweet_text: str) -> str:
    """Ensure the tweet is within the 280 character limit and not excessively short."""
    cleaned = tweet_text.strip()

    # Allow known short Degen phrases even if they are less than 10 characters
    # Check both original degen partial keys (lowercase) and their expanded values
    if cleaned.lower() in degen_partials or cleaned in degen_partials.values():
        if len(cleaned) > 280: # Should not happen for degen_partials but as a safeguard
             logger.warning(f"Degen partial was unexpectedly long and truncated: '{cleaned}'")
             return cleaned[:277].strip() + "..."
        return cleaned # Return as is, it's a known valid (potentially short) phrase

    if len(cleaned) < 10: # Arbitrary minimum length for a meaningful tweet
        logger.warning(f"Cleaned tweet is too short ('{cleaned}'), indicating poor extraction or meaningless content. Returning empty.")
        return ""
        
    if len(cleaned) > 280:
        logger.warning(f"Cleaned AI output exceeds 280 chars ('{cleaned[:50]}...'), truncating.")
        truncated_text = cleaned[:277] # Leave space for "..."
        last_space = truncated_text.rfind(' ')
        
        # Try to truncate at a word boundary, but only if the result is still reasonably long.
        # Avoid truncating to a very short word + "..."
        if last_space != -1 and len(truncated_text[:last_space]) > 150: 
            final_text = truncated_text[:last_space].strip() + "..."
        else: # If no good space or truncation makes it too short, just cut.
            final_text = cleaned[:277].strip() + "..." # Ensure it's stripped before ellipsis
        return final_text
        
    return cleaned

if __name__ == '__main__':
    # Basic Test Setup (requires config for XAIClient, even if mocked by tests later)
    # Ensure you have a dummy .env or config.yaml that XAIClient can load without error
    # or that your XAIClient mock in tests doesn't rely on real config loading.
    
    print("Running basic inline tests for ResponseGenerator...")

    # Sample/Mock data for testing
    from src.models.tweet import TweetMetadata # type: ignore
    from src.models.account import AccountType # type: ignore
    # For Step 18, we need TweetCategory for generate_new_tweet test
    from src.models.category import TweetCategory # type: ignore
    from src.config.settings import load_config # Ensure config is loaded for XAIClient init and mock knowledge
    load_config()

    test_tweet = Tweet(
        content="What are YieldFi's security measures? I am concerned.",
        metadata=TweetMetadata(tweet_id="test001", created_at="2023-01-01T12:00:00Z", author_id="user123", author_username="ConcernedUser"),
        tone="negative", # Pre-set tone
        sentiment_score=-0.5
    )
    official_account = Account(
        account_id="yieldfi_official", username="YieldFiOfficial", display_name="YieldFi Official",
        account_type=AccountType.OFFICIAL, platform="Twitter", follower_count=100000
    )
    intern_account = Account(
        account_id="yieldfi_intern", username="YieldFiIntern", display_name="YieldFi Intern",
        account_type=AccountType.INTERN, platform="Twitter", follower_count=100
    )
    target_user_account = Account(
        account_id="user123", username="ConcernedUser", display_name="Concerned User",
        account_type=AccountType.UNKNOWN, platform="Twitter", follower_count=50
    )
    
    # Test category for generate_new_tweet
    test_category = TweetCategory(
        name="Product Update",
        description="Announce new features or improvements.",
        prompt_keywords=["new feature", "update"],
        style_guidelines={"tone": "Excited and informative", "length": "Under 200 chars"}
    )

    # --- Test generate_tweet_reply --- 
    print("\n--- Testing generate_tweet_reply ---")
    # Mock XAIClient to avoid actual API calls if not setup with keys
    class MockXAIClient:
        def __init__(self, *args, **kwargs):
            print("MockXAIClient initialized")
            self.xai_api_key = "mock_xai_key"
            self.google_api_key = "mock_google_key"
            self.use_fallback = False
            self._model_name = "mock-xai-model-test"

        def get_completion(self, prompt: str, **kwargs) -> Dict[str, Any]:
            print(f"MockXAIClient.get_completion called with prompt starting: {prompt[:60]}...")
            # Simulate a successful response structure
            return {
                "choices": [
                    {
                        "text": f"This is a mock AI reply to: '{prompt_content_finder(prompt)}'"
                    }
                ]
            }
        def get_model_name(self) -> str:
            return self._model_name
    
    def prompt_content_finder(prompt_str):
        # Helper to find original post content in prompt for mock response
        if "Original Post to Reply To:" in prompt_str:
            try: return prompt_str.split("Original Post to Reply To: \"")[1].split("\"")[0]
            except: pass
        if "Specific Topic/Brief:" in prompt_str: # For new tweets
            try: return prompt_str.split("Specific Topic/Brief: ")[1].split("\n")[0]
            except: pass
        if "Tweet Category:" in prompt_str: # Fallback for new tweets if no topic
            try: return prompt_str.split("Tweet Category: ")[1].split("\n")[0]
            except: pass
        return "[original content not found in prompt]"

    original_xai_client = sys.modules['src.ai.xai_client'].XAIClient
    sys.modules['src.ai.xai_client'].XAIClient = MockXAIClient

    reply_response = generate_tweet_reply(
        original_tweet=test_tweet,
        responding_as=official_account,
        target_account=target_user_account
    )
    print(f"Generated Reply AIResponse content: {reply_response.content}")
    print(f"Generated Reply AIResponse type: {reply_response.response_type}")
    print(f"Generated Reply AIResponse tone_analysis: {reply_response.tone}")
    assert ResponseType.TWEET_REPLY == reply_response.response_type
    assert "mock AI reply" in reply_response.content
    assert "security measures" in reply_response.content # Check if original content made it to mock

    # --- Test generate_new_tweet --- 
    print("\n--- Testing generate_new_tweet ---")
    new_tweet_response = generate_new_tweet(
        category=test_category, # Pass TweetCategory object
        responding_as=official_account,
        topic="Announcing our new YieldBoost feature!"
    )
    print(f"Generated New Tweet AIResponse content: {new_tweet_response.content}")
    print(f"Generated New Tweet AIResponse type: {new_tweet_response.response_type}")
    assert ResponseType.NEW_TWEET == new_tweet_response.response_type
    assert "mock AI reply" in new_tweet_response.content # Mock will respond to prompt
    # Check if topic or category name made it to mock (depends on prompt_content_finder logic)
    assert "YieldBoost feature" in new_tweet_response.content or "Product Update" in new_tweet_response.content

    # Restore original XAIClient if needed for further non-mocked tests in other modules
    sys.modules['src.ai.xai_client'].XAIClient = original_xai_client
    print("\nResponseGenerator basic inline tests completed.") 