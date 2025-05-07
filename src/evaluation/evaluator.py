# Changelog:
# 2025-05-07 12:00 - Step 21 - Create evaluation framework evaluator.

"""
Evaluation framework for AI responses.
Defines Evaluator to run configured metrics against AIResponse objects.
"""

from typing import Optional, Dict
from src.evaluation.metrics import (
    relevance_score,
    tone_adherence_score,
    engagement_potential,
    factual_accuracy_score
)
from src.ai.tone_analyzer import analyze_tone
from src.models.response import AIResponse


class Evaluator:
    """
    Evaluator for computing evaluation metrics on AIResponse objects.
    """

    def evaluate_response(
        self,
        response: AIResponse,
        reference: str,
        desired_tone: Optional[str] = None,
        allow_factual: bool = False
    ) -> Dict[str, float]:
        """
        Evaluate an AIResponse against a reference response and optional desired tone.

        Args:
            response: The AIResponse object to evaluate.
            reference: Reference string to compare for relevance.
            desired_tone: Expected tone label (e.g., 'positive', 'neutral').
            allow_factual: If True, include factual_accuracy metric (placeholder).

        Returns:
            A dict mapping metric names to their computed float scores.
        """
        results: Dict[str, float] = {}
        # Relevance
        results["relevance"] = relevance_score(response.content, reference)

        # Tone adherence
        if desired_tone:
            # Use provided response tone if available, otherwise analyze content
            detected = getattr(response, 'tone', None) or analyze_tone(response.content).get("tone", "")
            results["tone_adherence"] = tone_adherence_score(detected, desired_tone)

        # Engagement potential
        results["engagement_potential"] = engagement_potential(response.content)

        # Factual accuracy
        if allow_factual:
            try:
                results["factual_accuracy"] = factual_accuracy_score()
            except NotImplementedError:
                results["factual_accuracy"] = float("nan")

        return results 