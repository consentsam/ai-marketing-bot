# Changelog:
# 2025-05-07 12:00 - Step 21 - Tests for evaluation evaluator.

import pytest
from src.evaluation.evaluator import Evaluator
from src.models.response import AIResponse, ResponseType
from datetime import datetime

@pytest.fixture
def dummy_response():
    return AIResponse(
        content="The quick brown fox jumps over the lazy dog",
        response_type=ResponseType.TWEET_REPLY,
        model_used="model",
        prompt_used="prompt",
        source_tweet_id="1",
        responding_as="user",
        target_account=None,
        generation_time=datetime.now(),
        tone="positive"
    )

def test_evaluate_response_basic(dummy_response):
    evaluator = Evaluator()
    results = evaluator.evaluate_response(dummy_response, reference="quick brown fox")
    assert "relevance" in results
    assert "engagement_potential" in results
    assert results["relevance"] > 0


def test_evaluate_response_with_tone(dummy_response):
    evaluator = Evaluator()
    results = evaluator.evaluate_response(dummy_response, reference="", desired_tone="positive")
    assert "tone_adherence" in results
    assert results["tone_adherence"] == 1.0


def test_evaluate_response_factual_accuracy_nan(dummy_response):
    evaluator = Evaluator()
    results = evaluator.evaluate_response(dummy_response, reference="", allow_factual=True)
    assert "factual_accuracy" in results
    assert str(results["factual_accuracy"]).lower() == "nan" 