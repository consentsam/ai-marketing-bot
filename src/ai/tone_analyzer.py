"""
Tone analyzer for the YieldFi AI Agent.

This module provides functionality for analyzing the tone of tweets.
"""

from typing import Dict, Any, Optional, Callable
from textblob import TextBlob
import os
import sys

# Ensure the test can find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.models.tweet import Tweet # type: ignore
from src.config.settings import get_config # type: ignore
from src.utils.logging import get_logger
from src.utils.error_handling import handle_api_error

# Logger instance
logger = get_logger('tone_analyzer')

# Define a type for the analysis functions
AnalysisFunction = Callable[[str], Dict[str, Any]]

def _analyze_with_textblob(text: str) -> Dict[str, Any]:
    """Analyzes text using TextBlob."""
    if not text: # Handle empty string to avoid potential issues
        return {
            "tone": "neutral",
            "sentiment_score": 0.0,
            "subjectivity": 0.0,
            "confidence": 1.0  # Confidence for empty string is high as it's definitively neutral
        }
    blob = TextBlob(text)
    sentiment = blob.sentiment
    
    tone = "neutral"
    if sentiment.polarity > 0.1: # Using a small threshold to avoid classifying very slight polarity as non-neutral
        tone = "positive"
    elif sentiment.polarity < -0.1:
        tone = "negative"
        
    return {
        "tone": tone,
        "sentiment_score": sentiment.polarity,
        "subjectivity": sentiment.subjectivity,
        "confidence": abs(sentiment.polarity) if sentiment.polarity != 0 else 1.0 # Using polarity as a proxy, or 1.0 for neutral
    }

def _analyze_with_xai(text: str) -> Dict[str, Any]:
    """Placeholder for analyzing text with xAI (Not Implemented)."""
    raise NotImplementedError("xAI analysis method is not yet implemented.")

def _analyze_with_google_palm(text: str) -> Dict[str, Any]:
    """Placeholder for analyzing text with Google PaLM (Not Implemented)."""
    raise NotImplementedError("Google PaLM analysis method is not yet implemented.")

_ANALYSIS_METHODS: Dict[str, AnalysisFunction] = {
    "textblob": _analyze_with_textblob,
    "xai": _analyze_with_xai,
    "google_palm": _analyze_with_google_palm,
}

def _get_analysis_method(method_name: Optional[str] = None) -> AnalysisFunction:
    """
    Retrieves the specified analysis function, or the default from config.
    Defaults to textblob if no method is specified or configured.
    """
    if method_name is None:
        method_name = get_config("tone_analysis.method", "textblob")
    
    selected_method = _ANALYSIS_METHODS.get(method_name.lower())
    if selected_method is None:
        print(f"Warning: Analysis method '{method_name}' not found. Defaulting to 'textblob'.") # Or raise a config error
        return _analyze_with_textblob
    return selected_method

def analyze_tone(text: str, method: Optional[str] = None) -> Dict[str, Any]:
    """
    Analyzes the tone of a given text using the specified or configured method.

    Args:
        text: The text to analyze.
        method: The analysis method to use (e.g., 'textblob', 'xai'). 
                If None, uses the method from config or defaults to 'textblob'.

    Returns:
        A dictionary containing:
            - 'tone': (str) 'positive', 'negative', or 'neutral'.
            - 'sentiment_score': (float) A score indicating sentiment (e.g., TextBlob polarity).
            - 'subjectivity': (float) A score indicating subjectivity (e.g., TextBlob subjectivity).
            - 'confidence': (float) A score indicating confidence in the tone classification.
    """
    analysis_func = _get_analysis_method(method)
    return analysis_func(text)

def analyze_tweet_tone(tweet: Tweet, method: Optional[str] = None) -> Tweet:
    """
    Analyzes the tone of a tweet's content and updates the tweet object.

    Args:
        tweet: The Tweet object to analyze.
        method: The analysis method to use. If None, uses the default.

    Returns:
        The updated Tweet object with 'tone' and 'sentiment_score' fields populated.
    """
    if not tweet.content:
        # Handle tweets with no content, perhaps set to neutral
        tweet.tone = "neutral"
        tweet.sentiment_score = 0.0
        # tweet.subjectivity = 0.0 # If we add this field to Tweet model
        return tweet

    analysis_result = analyze_tone(tweet.content, method=method)
    
    tweet.tone = analysis_result["tone"]
    tweet.sentiment_score = analysis_result["sentiment_score"]
    # If Tweet model is updated to include subjectivity:
    # tweet.subjectivity = analysis_result["subjectivity"] 
    
    return tweet

if __name__ == '__main__':
    # Simple test cases
    sample_texts = [
        ("YieldFi is amazing! Love the new features.", "positive"),
        ("I'm very unhappy with the recent changes.", "negative"),
        ("The market is stable today.", "neutral"),
        ("", "neutral"),
        ("This is a fantastic product, I am so happy!", "positive"),
        ("This is a terrible product, I am so sad.", "negative"),
        ("The sky is blue.", "neutral")
    ]

    print("Testing with TextBlob (default):")
    for text, expected_tone_category in sample_texts:
        result = analyze_tone(text)
        print(f"Text: \"{text}\"")
        print(f"  Expected: {expected_tone_category}")
        print(f"  Got: {result}")
        assert result["tone"] == expected_tone_category, f"Mismatch for '{text}'"
    
    print("\nTesting analyze_tweet_tone:")
    from src.models.tweet import TweetMetadata # type: ignore
    
    # Create a dummy tweet
    sample_tweet = Tweet(
        content="YieldFi's new update is groundbreaking and exciting!",
        metadata=TweetMetadata(tweet_id="123", created_at="2025-01-01T12:00:00Z", author_id="user1")
    )
    updated_tweet = analyze_tweet_tone(sample_tweet)
    print(f"Original Tweet Content: \"{sample_tweet.content}\"")
    print(f"  Analyzed Tone: {updated_tweet.tone}")
    print(f"  Sentiment Score: {updated_tweet.sentiment_score}")
    assert updated_tweet.tone == "positive"

    sample_tweet_neutral = Tweet(
        content="This is a statement.",
        metadata=TweetMetadata(tweet_id="124", created_at="2025-01-01T12:01:00Z", author_id="user2")
    )
    updated_tweet_neutral = analyze_tweet_tone(sample_tweet_neutral)
    print(f"Original Tweet Content: \"{updated_tweet_neutral.content}\"")
    print(f"  Analyzed Tone: {updated_tweet_neutral.tone}")
    print(f"  Sentiment Score: {updated_tweet_neutral.sentiment_score}")
    assert updated_tweet_neutral.tone == "neutral"


    print("\nTesting method selection (expect NotImplementedError for 'xai'):")
    try:
        analyze_tone("Test text", method="xai")
    except NotImplementedError as e:
        print(f"Correctly caught: {e}")
    except Exception as e:
        print(f"Incorrect exception for 'xai': {e}")
        assert False, "Should have raised NotImplementedError"

    print("\nAll basic inline tests passed.") 