# Changelog:
# 2025-05-07 12:00 - Step 21 - Create evaluation metrics module.

"""
Evaluation metrics for AIResponse objects.
Provides functions to assess response quality: relevance, tone adherence,
engagement potential, and placeholders for factual accuracy.
"""

from typing import Any
from collections import Counter
# Import tone analyzer for sentiment analysis
try:
    from src.ai.tone_analyzer import analyze_tone
except ImportError:
    from ai.tone_analyzer import analyze_tone


def jaccard_similarity(text1: str, text2: str) -> float:
    """
    Calculates Jaccard similarity between two texts based on token overlap.
    """
    tokens1 = set(text1.lower().split())
    tokens2 = set(text2.lower().split())
    # Handle empty cases
    if not tokens1 and not tokens2:
        return 1.0
    intersection = tokens1 & tokens2
    union = tokens1 | tokens2
    return len(intersection) / len(union)


def relevance_score(response_text: str, reference_text: str) -> float:
    """
    Computes relevance of a response relative to a reference using Jaccard similarity.
    """
    return jaccard_similarity(response_text, reference_text)


def tone_adherence_score(detected_tone: str, desired_tone: str) -> float:
    """
    Calculates a binary adherence score: 1.0 if detected tone matches desired tone, else 0.0.
    Comparison is case-insensitive.
    """
    return 1.0 if detected_tone.strip().lower() == desired_tone.strip().lower() else 0.0


def engagement_potential(response_text: str) -> float:
    """
    Estimates engagement potential based on sentiment analysis.
    Normalizes sentiment_score (-1 to 1) to a 0 to 1 range.
    """
    analysis = analyze_tone(response_text)
    sentiment = analysis.get("sentiment_score", 0.0)
    # Normalize [-1,1] to [0,1]
    return (sentiment + 1) / 2


def factual_accuracy_score(*args: Any, **kwargs: Any) -> float:
    """
    Placeholder for factual accuracy evaluation.
    Not implemented yet.
    """
    raise NotImplementedError("Factual accuracy evaluation not implemented yet.") 