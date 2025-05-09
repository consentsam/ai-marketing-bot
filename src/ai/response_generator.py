"""
Response generator for the YieldFi AI Agent.

This module provides the core functionality for generating AI responses.
"""

from typing import Dict, Any, Optional
import os
import sys
from datetime import datetime, timezone

# Ensure the test can find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models.tweet import Tweet # type: ignore
from src.models.account import Account, AccountType # type: ignore
from src.models.response import AIResponse, ResponseType # type: ignore
from src.models.category import TweetCategory # Added for Step 18
from src.ai.xai_client import XAIClient, APIError as XAIAPIError # type: ignore
from src.ai.prompt_engineering import generate_interaction_prompt, generate_new_tweet_prompt # type: ignore
from src.ai.tone_analyzer import analyze_tweet_tone # type: ignore
from src.utils.logging import get_logger # type: ignore
# from src.knowledge.retrieval import KnowledgeRetriever # Step 11 - Mock for now

logger = get_logger(__name__)

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
    generate_image: bool = False
) -> AIResponse:
    """
    Generates a reply to a given tweet.
    Orchestrates tone analysis, knowledge retrieval (mocked), prompt engineering, and AI client call.
    """
    # Use provided Account for responding_as
    responding_as_account = responding_as

    logger.info(f"Generating reply for tweet ID: {original_tweet.metadata.tweet_id} as {responding_as_account.username} (Type: {responding_as_account.account_type.value})")
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

        # 3. Generate prompt
        logger.info("Generating interaction prompt...")
        prompt_str = generate_interaction_prompt(
            original_post_content=original_tweet.content,
            active_account_info=responding_as_account,
            target_account_info=target_account,
            yieldfi_knowledge_snippet=knowledge_snippet,
            interaction_details=interaction_details if interaction_details else {},
            platform=platform
        )
        logger.debug(f"Generated interaction prompt: {prompt_str[:300]}...")

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
                ai_generated_content = _clean_ai_raw_output(raw_content)
                logger.info(f"Cleaned text output (reply, first 100 chars): '{ai_generated_content[:100]}...'")
                if len(ai_generated_content) < 30 or ai_generated_content.endswith(",") or ai_generated_content[-1] not in ".!?" and len(ai_generated_content) < 100:
                    logger.warning(f"AI reply may be incomplete or cut off: '{ai_generated_content}'")
            elif choice.get('message'):
                message_data = choice['message']
                if message_data.get('content') and message_data['content'].strip():
                    raw_content = message_data['content'].strip()
                    logger.info(f"Extracted 'content' from message: '{raw_content[:100]}...'")
                    logger.debug(f"Full raw AI output (reply, from 'message.content'): {raw_content}")
                    # Clean the response
                    ai_generated_content = _clean_ai_raw_output(raw_content)
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
                ai_generated_content = _clean_ai_raw_output(ai_generated_content)
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
        tone=final_tone
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
    return response

def generate_new_tweet(
    category,
    responding_as: Account,
    topic: Optional[str] = None,
    knowledge_retriever: Optional[MockKnowledgeRetriever] = None,  # Using Mock for now
    platform: str = "Twitter",
    additional_instructions: Optional[Dict[str, Any]] = None,
    generate_image: bool = False
) -> AIResponse:
    """
    Generates a new tweet based on a category, topic, and other details.
    Orchestrates knowledge retrieval (mocked), prompt engineering, and AI client call.
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

        # 2. Generate prompt using TweetCategory object
        logger.info("Generating new tweet prompt...")
        prompt_str = generate_new_tweet_prompt(
            category=original_category,  # Pass original category (string or TweetCategory)
            topic=topic,
            active_account_info=responding_as_account,
            yieldfi_knowledge_snippet=knowledge_snippet,
            platform=platform,
            additional_instructions=additional_instructions
        )
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
                ai_generated_content = _clean_ai_raw_output(raw_content)
                logger.info(f"Cleaned text output (new tweet, first 100 chars): '{ai_generated_content[:100]}...'")
                if len(ai_generated_content) < 30 or ai_generated_content.endswith(",") or ai_generated_content[-1] not in ".!?" and len(ai_generated_content) < 100:
                    logger.warning(f"AI reply may be incomplete or cut off: '{ai_generated_content}'")
            elif choice.get('message'):
                message_data = choice['message']
                if message_data.get('content') and message_data['content'].strip():
                    raw_content = message_data['content'].strip()
                    logger.info(f"Extracted 'content' from message (new tweet): '{raw_content[:100]}...'")
                    logger.debug(f"Full raw AI output (new tweet, from 'message.content'): {raw_content}")
                    # Clean the response
                    ai_generated_content = _clean_ai_raw_output(raw_content)
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
                ai_generated_content = _clean_ai_raw_output(ai_generated_content)
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
            "error_message": response_error  # Add error message to AIResponse object
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
    return final_response

def _clean_ai_raw_output(raw_output: str) -> str:
    """
    Cleans the raw AI output to extract just the tweet text.
    
    This function handles various formats that AI might return, including:
    - Prefixes like "Assistant:" or "AI:"
    - Internal dialogue/reasoning
    - Multiple tweet versions/drafts
    
    Args:
        raw_output: The raw text from the AI model
        
    Returns:
        The cleaned tweet text only
    """
    logger.debug(f"Cleaning raw AI output (original): '{raw_output}'")

    lines = raw_output.splitlines()
    cleaned_lines = []
    tweet_started = False

    # Attempt to remove conversational prefixes and only keep the core message
    # This is more aggressive now.
    common_prefixes = [
        "Assistant:", "AI:", "Okay, here's a tweet:", "Sure, here's the tweet:",
        "Tweet:", "Response:", "Reply:", "Here's your tweet:"
    ]
    
    temp_cleaned_output = raw_output.strip()

    # First, remove any explicit prefixes if the whole response starts with them
    for prefix in common_prefixes:
        if temp_cleaned_output.lower().startswith(prefix.lower()):
            temp_cleaned_output = temp_cleaned_output[len(prefix):].strip()
            logger.debug(f"Removed prefix '{prefix}'. Output is now: '{temp_cleaned_output[:100]}...'")
            break # Only remove one prefix

    # Now, if "Assistant:" or "AI:" is still in the text, assume it's meta-commentary
    # and take everything before it. This is for cases like "Tweet text Assistant: reasoning"
    meta_markers = ["Assistant:", "AI:", "\n\nAssistant:", "\n\nAI:"] # Add newline versions
    for marker in meta_markers:
        if marker in temp_cleaned_output:
            parts = temp_cleaned_output.split(marker, 1)
            potential_tweet = parts[0].strip()
            # Only take the part before the marker if it's substantial
            if len(potential_tweet) > 20 or len(parts) == 1 : # Check if the part before is long enough or it's the only part
                 temp_cleaned_output = potential_tweet
                 logger.debug(f"Split by '{marker}'. Output is now: '{temp_cleaned_output[:100]}...'")
                 break
            else: # If part before marker is too short, it might be the AI failing, keep original
                logger.debug(f"Part before '{marker}' is too short ('{potential_tweet}'). Keeping original for this marker.")


    # Remove leading/trailing quotes that AI sometimes adds
    if temp_cleaned_output.startswith('"') and temp_cleaned_output.endswith('"'):
        temp_cleaned_output = temp_cleaned_output[1:-1].strip()
        logger.debug(f"Removed surrounding quotes. Output is now: '{temp_cleaned_output[:100]}...'")
    
    cleaned = temp_cleaned_output

    # Final length check
    if len(cleaned) > 280:
        logger.warning(f"Cleaned AI output still exceeds 280 chars ('{cleaned[:50]}...'), truncating to 280.")
        cleaned = cleaned[:280].strip() # Strip again after truncating
        # Try to avoid cutting mid-word if possible (simple approach)
        if ' ' in cleaned:
            cleaned = cleaned.rsplit(' ', 1)[0] 

    logger.info(f"Final cleaned output: '{cleaned}'")
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