# src/evaluation/__init__.py - Created 2025-05-07 

# Changelog:
# - 2025-05-16: Updated for Step 21 (Evaluation Framework).
#   - Exported Evaluator and calculate_* metric functions.
# - 2025-05-07: Initial __init__.py for evaluation module (original entry from file).

"""
Initialization file for the YieldFi AI Agent evaluation module.

This module provides tools and frameworks for evaluating the performance
of AI-generated content, including metrics for relevance, tone, accuracy, etc.
"""

# Core components to be publicly available from the evaluation module
from .metrics import (
    calculate_tone_match_score,
    calculate_relevance_score,
    calculate_factual_accuracy_score
)
from .evaluator import Evaluator

__all__ = [
    "calculate_tone_match_score",
    "calculate_relevance_score",
    "calculate_factual_accuracy_score",
    "Evaluator"
] 