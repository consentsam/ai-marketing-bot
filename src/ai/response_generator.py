"""
Response generator for the YieldFi AI Agent.

This module provides the core functionality for generating AI responses.
"""

from typing import Dict, Any, Optional

from src.models.tweet import Tweet
from src.models.account import Account, AccountType
from src.models.response import AIResponse, ResponseType
from src.ai.tone_analyzer import analyze_tone, analyze_tweet_tone
from src.ai.prompt_engineering import create_prompt
from src.ai.xai_client import XAIClient
from src.utils.logging import get_logger
from src.utils.error_handling import handle_api_error

# Logger instance
logger = get_logger('response_generator')


@handle_api_error
def generate_tweet_reply(
    tweet: Tweet,
    responding_as: str = "official",
    target_account: Optional[Account] = None,
    tone_override: Optional[str] = None,
    yieldfi_context: Optional[Dict[str, Any]] = None,
    max_length: int = 280
) -> AIResponse:
    """Generate a reply to a tweet.
    
    Args:
        tweet: Tweet to respond to
        responding_as: Account type responding (e.g., "official", "intern")
        target_account: Target account to respond to
        tone_override: Override the detected tone
        yieldfi_context: Additional context about YieldFi
        max_length: Maximum length of the response
        
    Returns:
        Generated AIResponse
    """
    # Make sure the tweet has been analyzed for tone
    if tweet.tone is None:
        tweet = analyze_tweet_tone(tweet)
    
    # Determine the tone for the response
    response_tone = tone_override
    if response_tone is None:
        # Match positive with positive, neutral with neutral
        # But for negative tweets, respond with a balanced tone
        if tweet.tone == "negative":
            response_tone = "balanced"
        else:
            response_tone = tweet.tone
    
    # Create the prompt
    prompt = create_prompt(
        tweet=tweet,
        response_type=ResponseType.TWEET_REPLY,
        responding_as=responding_as,
        target_account=target_account,
        tone=response_tone,
        max_length=max_length,
        yieldfi_context=yieldfi_context
    )
    
    # Generate the response using the AI client
    xai_client = XAIClient()
    content = xai_client.generate_text(
        prompt=prompt,
        max_tokens=max_length,
        temperature=0.7
    )
    
    # Create and return the response object
    return AIResponse(
        content=content,
        response_type=ResponseType.TWEET_REPLY,
        model_used=xai_client.use_fallback and "google_palm" or "xai",
        prompt_used=prompt,
        source_tweet_id=tweet.metadata.tweet_id,
        responding_as=responding_as,
        target_account=target_account.username if target_account else None,
        tone=response_tone,
        max_length=max_length
    )


@handle_api_error
def generate_new_tweet(
    category: str,
    responding_as: str = "official",
    topic: Optional[str] = None,
    tone: Optional[str] = None,
    yieldfi_context: Optional[Dict[str, Any]] = None,
    max_length: int = 280
) -> AIResponse:
    """Generate a new tweet.
    
    Args:
        category: Category of the tweet (e.g., "announcement", "product-update")
        responding_as: Account type responding (e.g., "official", "intern")
        topic: Specific topic for the tweet
        tone: Desired tone of the tweet
        yieldfi_context: Additional context about YieldFi
        max_length: Maximum length of the tweet
        
    Returns:
        Generated AIResponse
    """
    # Map category to response type
    response_type = ResponseType.NEW_TWEET
    if category.lower() == "announcement":
        response_type = ResponseType.ANNOUNCEMENT
    elif category.lower() in ["product-update", "product_update"]:
        response_type = ResponseType.PRODUCT_UPDATE
    elif category.lower() in ["community-update", "community_update"]:
        response_type = ResponseType.COMMUNITY_UPDATE
    elif category.lower() == "event":
        response_type = ResponseType.EVENT
    
    # If no tone specified, use default for the category
    if tone is None:
        if response_type == ResponseType.ANNOUNCEMENT:
            tone = "professional"
        elif response_type == ResponseType.PRODUCT_UPDATE:
            tone = "enthusiastic"
        elif response_type == ResponseType.COMMUNITY_UPDATE:
            tone = "friendly"
        elif response_type == ResponseType.EVENT:
            tone = "excited"
        else:
            tone = "balanced"
    
    # Build context including the topic if provided
    context = yieldfi_context or {}
    if topic:
        context["topic"] = topic
    
    # Create the prompt
    prompt = create_prompt(
        tweet=None,  # No tweet to respond to
        response_type=response_type,
        responding_as=responding_as,
        target_account=None,  # No specific target
        tone=tone,
        max_length=max_length,
        yieldfi_context=context
    )
    
    # Generate the response using the AI client
    xai_client = XAIClient()
    content = xai_client.generate_text(
        prompt=prompt,
        max_tokens=max_length,
        temperature=0.7
    )
    
    # Create and return the response object
    return AIResponse(
        content=content,
        response_type=response_type,
        model_used=xai_client.use_fallback and "google_palm" or "xai",
        prompt_used=prompt,
        responding_as=responding_as,
        tone=tone,
        max_length=max_length,
        tags=[category] + ([topic] if topic else [])
    ) 