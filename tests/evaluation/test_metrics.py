# Changelog:
# 2025-05-07 12:00 - Step 21 - Tests for evaluation metrics module.

import pytest
from src.evaluation.metrics import (
    jaccard_similarity,
    relevance_score,
    tone_adherence_score,
    engagement_potential,
    factual_accuracy_score
)

def test_jaccard_similarity_identical():
    assert jaccard_similarity("hello world", "hello world") == 1.0


def test_jaccard_similarity_disjoint():
    assert jaccard_similarity("foo", "bar") == 0.0


def test_relevance_score():
    resp = "quick brown fox"
    ref = "quick fox"
    # Intersection {'quick','fox'}=2, union {'quick','brown','fox'}=3
    assert abs(relevance_score(resp, ref) - 2/3) < 1e-6


def test_tone_adherence_score_match():
    assert tone_adherence_score("Positive", "positive") == 1.0


def test_tone_adherence_score_mismatch():
    assert tone_adherence_score("neutral", "negative") == 0.0

@pytest.mark.parametrize("text,low,high", [
    ("I love this product!", 0.6, 1.0),
    ("I hate this service!", 0.0, 0.4),
])
def test_engagement_potential(text, low, high):
    score = engagement_potential(text)
    assert low <= score < high


def test_factual_accuracy_not_implemented():
    with pytest.raises(NotImplementedError):
        factual_accuracy_score() 