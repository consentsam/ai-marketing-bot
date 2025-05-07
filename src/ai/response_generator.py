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
from src.models.account import Account # type: ignore
from src.models.response import AIResponse, ResponseType # type: ignore
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

    def search_knowledge_for_topic(self, topic: str, category: Optional[str] = None) -> Optional[str]:
        logger.info(f"MockKnowledgeRetriever: Received topic '{topic}' for category '{category}'. Returning mock knowledge.")
        if "new product" in topic.lower():
            return "Our latest product, YieldBoost, offers enhanced returns through automated strategies."
        return "YieldFi continually innovates to bring value to its users."

# --- Mocked Knowledge Retriever --- END

def generate_tweet_reply(
    original_tweet: Tweet,
    responding_as: Account,
    target_account: Optional[Account] = None,
    platform: str = "Twitter",
    interaction_details: Optional[Dict[str, Any]] = None,
    # knowledge_retriever: Optional[KnowledgeRetriever] = None # For Step 11
    knowledge_retriever: Optional[MockKnowledgeRetriever] = None # Using Mock for now
) -> AIResponse:
    """
    Generates a reply to a given tweet.
    Orchestrates tone analysis, knowledge retrieval (mocked), prompt engineering, and AI client call.
    """
    logger.info(f"Generating reply for tweet ID: {original_tweet.metadata.tweet_id} as {responding_as.username}")
    prompt_str = ""
    ai_generated_content = "[Error: Could not generate AI response]"
    model_used = "Unknown"
    final_tone = original_tweet.tone

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

        # 3. Generate prompt
        prompt_str = generate_interaction_prompt(
            original_post_content=original_tweet.content,
            active_account_info=responding_as,
            target_account_info=target_account,
            yieldfi_knowledge_snippet=knowledge_snippet,
            interaction_details=interaction_details if interaction_details else {},
            platform=platform,
            original_post_tone=final_tone
        )
        logger.debug(f"Generated interaction prompt: {prompt_str[:300]}...")

        # 4. Call AI client
        # This assumes XAIClient is properly configured (Step 6)
        xai_client = XAIClient() # API keys loaded from config within XAIClient
        model_used = "xAI (or fallback)" # Placeholder, XAIClient might provide more detail
        
        ai_response_data = xai_client.get_completion(prompt=prompt_str)
        
        # Extract content - this depends on the actual structure of xAI/PaLM response
        # Assuming a common structure like response.get('choices')[0].get('text') or similar
        if ai_response_data.get('choices') and isinstance(ai_response_data['choices'], list) and len(ai_response_data['choices']) > 0:
            choice = ai_response_data['choices'][0]
            if choice.get('text'):
                ai_generated_content = choice['text'].strip()
            elif choice.get('message') and choice['message'].get('content'): # For chat-like models
                 ai_generated_content = choice['message']['content'].strip()
            else:
                logger.warning(f"Could not extract text from AI response choice: {choice}")
                ai_generated_content = "[Warning: AI response format unclear]"
        elif ai_response_data.get('candidates') and isinstance(ai_response_data['candidates'], list) and len(ai_response_data['candidates']) > 0:
             # Fallback for Google PaLM style response (text-bison-001 example)
            candidate = ai_response_data['candidates'][0]
            if candidate.get('output'):
                ai_generated_content = candidate['output'].strip()
            else:
                logger.warning(f"Could not extract text from AI response candidate: {candidate}")
                ai_generated_content = "[Warning: AI response format unclear (PaLM candidate)]"
        else:
            logger.warning(f"AI response structure not recognized for content extraction: {ai_response_data}")
            ai_generated_content = "[Warning: AI response structure not recognized]"

        logger.info(f"Successfully generated AI reply: {ai_generated_content[:100]}...")

    except XAIAPIError as e:
        logger.error(f"XAIClient APIError in generate_tweet_reply: {e}", exc_info=True)
        ai_generated_content = f"[Error: AI API call failed - {e.message}]"
    except Exception as e:
        logger.error(f"Unexpected error in generate_tweet_reply: {e}", exc_info=True)
        ai_generated_content = f"[Error: Unexpected error during response generation - {str(e)}]"

    return AIResponse(
        content=ai_generated_content,
        response_type=ResponseType.TWEET_REPLY,
        model_used=model_used,
        prompt_used=prompt_str,
        source_tweet_id=original_tweet.metadata.tweet_id,
        responding_as=responding_as.account_type.value,
        target_account=target_account.username if target_account else None,
        generation_time=datetime.now(timezone.utc),
        tone=final_tone # Tone of the original post, or could be tone of the response if analyzed
    )

def generate_new_tweet(
    category: str,
    responding_as: Account,
    topic: Optional[str] = None,
    platform: str = "Twitter",
    additional_instructions: Optional[Dict[str, Any]] = None,
    # knowledge_retriever: Optional[KnowledgeRetriever] = None # For Step 11
    knowledge_retriever: Optional[MockKnowledgeRetriever] = None # Using Mock for now
) -> AIResponse:
    """
    Generates a new tweet based on a category, topic, and other details.
    Orchestrates knowledge retrieval (mocked), prompt engineering, and AI client call.
    """
    logger.info(f"Generating new '{category}' tweet on topic '{topic}' as {responding_as.username}")
    prompt_str = ""
    ai_generated_content = "[Error: Could not generate AI response]"
    model_used = "Unknown"

    try:
        # 1. Retrieve relevant knowledge (Mocked for now)
        knowledge_snippet: Optional[str] = None
        # For Step 11: if knowledge_retriever:
        current_retriever = knowledge_retriever if knowledge_retriever else MockKnowledgeRetriever()
        knowledge_query = topic if topic else category
        knowledge_snippet = current_retriever.search_knowledge_for_topic(knowledge_query, category)
        if knowledge_snippet:
            logger.info(f"Retrieved knowledge snippet for new tweet: {knowledge_snippet[:100]}...")

        # 2. Generate prompt
        prompt_str = generate_new_tweet_prompt(
            category=category,
            topic=topic,
            active_account_info=responding_as,
            yieldfi_knowledge_snippet=knowledge_snippet,
            platform=platform,
            additional_instructions=additional_instructions
        )
        logger.debug(f"Generated new tweet prompt: {prompt_str[:300]}...")

        # 3. Call AI client
        xai_client = XAIClient()
        model_used = "xAI (or fallback)"
        ai_response_data = xai_client.get_completion(prompt=prompt_str)

        # Extract content (same logic as generate_tweet_reply)
        if ai_response_data.get('choices') and isinstance(ai_response_data['choices'], list) and len(ai_response_data['choices']) > 0:
            choice = ai_response_data['choices'][0]
            if choice.get('text'):
                ai_generated_content = choice['text'].strip()
            elif choice.get('message') and choice['message'].get('content'):
                 ai_generated_content = choice['message']['content'].strip()
            else:
                ai_generated_content = "[Warning: AI response format unclear]"
        elif ai_response_data.get('candidates') and isinstance(ai_response_data['candidates'], list) and len(ai_response_data['candidates']) > 0:
            candidate = ai_response_data['candidates'][0]
            if candidate.get('output'):
                ai_generated_content = candidate['output'].strip()
            else:
                ai_generated_content = "[Warning: AI response format unclear (PaLM candidate)]"
        else:
            ai_generated_content = "[Warning: AI response structure not recognized]"

        logger.info(f"Successfully generated new AI tweet: {ai_generated_content[:100]}...")

    except XAIAPIError as e:
        logger.error(f"XAIClient APIError in generate_new_tweet: {e}", exc_info=True)
        ai_generated_content = f"[Error: AI API call failed - {e.message}]"
    except Exception as e:
        logger.error(f"Unexpected error in generate_new_tweet: {e}", exc_info=True)
        ai_generated_content = f"[Error: Unexpected error during new tweet generation - {str(e)}]"

    return AIResponse(
        content=ai_generated_content,
        response_type=ResponseType.NEW_TWEET, # Or more specific based on category?
        model_used=model_used,
        prompt_used=prompt_str,
        responding_as=responding_as.account_type.value,
        target_account=None,
        generation_time=datetime.now(timezone.utc),
        tone=None # Tone of new tweet could be analyzed post-generation if needed
    )

if __name__ == '__main__':
    # Basic Test Setup (requires config for XAIClient, even if mocked by tests later)
    # Ensure you have a dummy .env or config.yaml that XAIClient can load without error
    # or that your XAIClient mock in tests doesn't rely on real config loading.
    
    print("Running basic inline tests for ResponseGenerator...")

    # Sample/Mock data for testing
    from src.models.tweet import TweetMetadata # type: ignore
    from src.models.account import AccountType # type: ignore

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

    # --- Test generate_tweet_reply --- 
    print("\n--- Testing generate_tweet_reply ---")
    # Mock XAIClient to avoid actual API calls if not setup with keys
    class MockXAIClient:
        def __init__(self, *args, **kwargs):
            print("MockXAIClient initialized")
            self.xai_api_key = "mock_xai_key"
            self.google_api_key = "mock_google_key"
            self.use_fallback = False

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
    
    def prompt_content_finder(prompt_str):
        # Helper to find original post content in prompt for mock response
        if "Original Post to Reply To:" in prompt_str:
            try: return prompt_str.split("Original Post to Reply To: \"")[1].split("\"")[0]
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
    print(f"Generated Reply AIResponse tone (of original): {reply_response.tone}")
    assert ResponseType.TWEET_REPLY == reply_response.response_type
    assert "mock AI reply" in reply_response.content
    assert "security measures" in reply_response.content # Check if original content made it to mock

    # --- Test generate_new_tweet --- 
    print("\n--- Testing generate_new_tweet ---")
    new_tweet_response = generate_new_tweet(
        category="Product Update",
        responding_as=official_account,
        topic="Announcing our new YieldBoost feature!"
    )
    print(f"Generated New Tweet AIResponse content: {new_tweet_response.content}")
    print(f"Generated New Tweet AIResponse type: {new_tweet_response.response_type}")
    assert ResponseType.NEW_TWEET == new_tweet_response.response_type
    assert "mock AI reply" in new_tweet_response.content # Mock will respond to prompt
    assert "YieldBoost feature" in new_tweet_response.content # Check if topic made it to mock

    # Restore original XAIClient if needed for further non-mocked tests in other modules
    sys.modules['src.ai.xai_client'].XAIClient = original_xai_client
    print("\nResponseGenerator basic inline tests completed.") 