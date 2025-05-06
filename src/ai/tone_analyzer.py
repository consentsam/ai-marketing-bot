"""
Tone analyzer for the YieldFi AI Agent.

This module provides functionality for analyzing the tone of tweets.
"""

from typing import Dict, Any, Optional

from textblob import TextBlob

from src.config.settings import get_config
from src.models.tweet import Tweet
from src.utils.logging import get_logger
from src.utils.error_handling import handle_api_error

# Logger instance
logger = get_logger('tone_analyzer')


@handle_api_error
def analyze_tone(text: str, method: Optional[str] = None) -> Dict[str, Any]:
    """Analyze the tone of a text.
    
    Args:
        text: Text to analyze
        method: Method to use for analysis (if None, will be loaded from configuration)
        
    Returns:
        Dictionary containing tone analysis results
    """
    if not text:
        return {
            'tone': 'neutral',
            'sentiment': 0.0,
            'subjectivity': 0.0,
            'confidence': 0.0
        }
    
    # Get the analysis method from configuration if not provided
    if method is None:
        method = get_config('tone_analysis.method', 'textblob')
    
    logger.debug("Analyzing tone of text: %s (method: %s)", text[:50], method)
    
    if method == 'textblob':
        return _analyze_with_textblob(text)
    elif method == 'xai':
        return _analyze_with_xai(text)
    elif method == 'google_palm':
        return _analyze_with_google_palm(text)
    else:
        logger.warning("Unknown tone analysis method: %s, using textblob", method)
        return _analyze_with_textblob(text)


def _analyze_with_textblob(text: str) -> Dict[str, Any]:
    """Analyze the tone of a text using TextBlob.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary containing tone analysis results
    """
    try:
        blob = TextBlob(text)
        sentiment = blob.sentiment.polarity
        subjectivity = blob.sentiment.subjectivity
        
        # Determine tone based on sentiment
        if sentiment > 0.3:
            tone = 'positive'
        elif sentiment < -0.3:
            tone = 'negative'
        else:
            tone = 'neutral'
        
        # Determine confidence based on subjectivity
        # Higher subjectivity means more opinionated, so we use it as confidence
        confidence = subjectivity
        
        return {
            'tone': tone,
            'sentiment': sentiment,
            'subjectivity': subjectivity,
            'confidence': confidence
        }
    except Exception as e:
        logger.error("Error analyzing tone with TextBlob: %s", str(e))
        return {
            'tone': 'neutral',
            'sentiment': 0.0,
            'subjectivity': 0.0,
            'confidence': 0.0,
            'error': str(e)
        }


def _analyze_with_xai(text: str) -> Dict[str, Any]:
    """Analyze the tone of a text using xAI.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary containing tone analysis results
    """
    # Placeholder implementation
    # When the actual xAI API is available, this will be replaced with real API calls
    logger.info("Analyzing tone with xAI API (placeholder)")
    
    # For now, fall back to TextBlob
    logger.info("Falling back to TextBlob for tone analysis")
    return _analyze_with_textblob(text)


def _analyze_with_google_palm(text: str) -> Dict[str, Any]:
    """Analyze the tone of a text using Google PaLM.
    
    Args:
        text: Text to analyze
        
    Returns:
        Dictionary containing tone analysis results
    """
    try:
        from langchain.llms import GooglePalm
        
        google_api_key = get_config('ai.google_palm_api_key', '')
        if not google_api_key:
            logger.error("No Google PaLM API key provided")
            return _analyze_with_textblob(text)
        
        # Create Google PaLM client
        llm = GooglePalm(
            google_api_key=google_api_key,
            temperature=0.1,  # Low temperature for more deterministic results
        )
        
        # Create the prompt for tone analysis
        prompt = f"""
        Analyze the tone of the following text. Return the result as a JSON object with the following keys:
        - tone: One of "positive", "negative", or "neutral"
        - sentiment: A number between -1 (negative) and 1 (positive)
        - subjectivity: A number between 0 (objective) and 1 (subjective)
        - confidence: A number between 0 (low confidence) and 1 (high confidence)
        
        Text to analyze: "{text}"
        
        JSON result:
        """
        
        # Generate the analysis
        response = llm(prompt)
        
        # Parse the response
        import json
        try:
            result = json.loads(response)
            return {
                'tone': result.get('tone', 'neutral'),
                'sentiment': float(result.get('sentiment', 0.0)),
                'subjectivity': float(result.get('subjectivity', 0.0)),
                'confidence': float(result.get('confidence', 0.0))
            }
        except json.JSONDecodeError:
            logger.error("Error parsing JSON response from Google PaLM: %s", response)
            return _analyze_with_textblob(text)
        
    except ImportError:
        logger.error("Google PaLM not installed, falling back to TextBlob")
        return _analyze_with_textblob(text)
    except Exception as e:
        logger.error("Error analyzing tone with Google PaLM: %s", str(e))
        return _analyze_with_textblob(text)


def analyze_tweet_tone(tweet: Tweet) -> Tweet:
    """Analyze the tone of a tweet and update its tone attribute.
    
    Args:
        tweet: Tweet to analyze
        
    Returns:
        The updated Tweet object
    """
    # Check if tone analysis is enabled
    if not get_config('tone_analysis.enabled', True):
        return tweet
    
    # Skip analysis if tone is already set
    if tweet.tone is not None:
        return tweet
    
    # Analyze the tone
    analysis = analyze_tone(tweet.content)
    
    # Update the tweet
    tweet.tone = analysis['tone']
    tweet.sentiment_score = analysis['sentiment']
    
    return tweet 