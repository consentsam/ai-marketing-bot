# Changelog:
# - 2025-05-16: Initial creation for Step 21 (Evaluation Framework).
#   - Added unit tests for the Evaluator class.

import unittest
import json
from typing import List, Dict, Any, Optional, cast

# Assuming models and Evaluator are in src directory, adjust if needed for your test runner
try:
    from src.models.response import AIResponse # Assuming AIResponse has content and tone attributes
    from src.evaluation.evaluator import Evaluator
except ImportError:
    # Fallback for local execution if PYTHONPATH is not set
    from models.response import AIResponse # type: ignore
    from evaluation.evaluator import Evaluator # type: ignore

# Mock AIResponse class for testing, as the actual AIResponse might have more dependencies
class MockAIResponseForEval:
    def __init__(self, content: str, tone: Optional[str]):
        self.content = content
        self.tone = tone # Analyzed tone of the AI's own response

    def to_dict(self) -> Dict[str, Any]: # Example method, if your AIResponse has it
        return {"content": self.content, "tone": self.tone}

class TestEvaluator(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        """Load golden set data once for all tests."""
        cls.golden_set_data: List[Dict[str, Any]] = []
        try:
            # Path assumes tests are run from the project root directory
            # Adjust if your test runner has a different working directory
            with open("data/input/evaluation_golden_set.json", 'r') as f:
                cls.golden_set_data = json.load(f)
        except FileNotFoundError:
            print("Warning: data/input/evaluation_golden_set.json not found. Some tests may be skipped or fail.")
        except json.JSONDecodeError:
            print("Warning: Error decoding data/input/evaluation_golden_set.json. Some tests may be skipped or fail.")

    def test_evaluator_initialization(self):
        evaluator_default = Evaluator()
        self.assertListEqual(sorted(evaluator_default.metrics_to_run), sorted(['tone_match', 'relevance', 'factual_accuracy']))

        evaluator_specific = Evaluator(metrics_to_run=['tone_match', 'factual_accuracy'])
        self.assertListEqual(sorted(evaluator_specific.metrics_to_run), sorted(['factual_accuracy', 'tone_match']))

        evaluator_with_unknown = Evaluator(metrics_to_run=['tone_match', 'unknown_metric', 'relevance'])
        self.assertListEqual(sorted(evaluator_with_unknown.metrics_to_run), sorted(['relevance', 'tone_match']))
        # Add a check for the warning print if possible, or trust it was printed.

    def test_evaluate_response_all_metrics_sample1(self):
        if not self.golden_set_data:
            self.skipTest("Golden set data not loaded.")

        sample = self.golden_set_data[0]
        ai_response = MockAIResponseForEval(
            content=sample["ai_response_content"],
            tone=sample["ai_response_analyzed_tone"]
        )
        # Cast to AIResponse for the evaluator, our mock is compatible for content & tone
        eval_result = Evaluator().evaluate_response(
            ai_response=cast(AIResponse, ai_response),
            original_tweet_content=sample["original_tweet_content"],
            knowledge_snippet_used=sample.get("knowledge_snippet_used"),
            ground_truth_data=sample["ground_truth_data"]
        )
        
        self.assertIn('tone_match', eval_result)
        self.assertIn('relevance', eval_result)
        self.assertIn('factual_accuracy', eval_result)
        self.assertAlmostEqual(eval_result['tone_match'], 1.0) # Based on sample_eval_1 data
        self.assertGreaterEqual(eval_result['relevance'], 0.0) # Actual value depends on NLTK processing
        self.assertLessEqual(eval_result['relevance'], 1.0)
        self.assertAlmostEqual(eval_result['factual_accuracy'], 1.0) # All 3 facts should be found

    def test_evaluate_response_specific_metrics_sample2(self):
        if len(self.golden_set_data) < 2:
            self.skipTest("Golden set data does not contain enough samples.")

        sample = self.golden_set_data[1]
        ai_response = MockAIResponseForEval(
            content=sample["ai_response_content"],
            tone=sample["ai_response_analyzed_tone"] # "slightly_positive"
        )
        evaluator = Evaluator(metrics_to_run=['tone_match', 'factual_accuracy'])
        eval_result = evaluator.evaluate_response(
            ai_response=cast(AIResponse, ai_response),
            original_tweet_content=sample["original_tweet_content"],
            knowledge_snippet_used=sample.get("knowledge_snippet_used"),
            ground_truth_data=sample["ground_truth_data"]
        )

        self.assertIn('tone_match', eval_result)
        self.assertNotIn('relevance', eval_result) # Relevance was not in metrics_to_run
        self.assertIn('factual_accuracy', eval_result)
        
        # Expected tone: neutral, Actual: slightly_positive -> mismatch
        self.assertAlmostEqual(eval_result['tone_match'], 0.0) 
        # Facts: "TVL is $150M" (found), "audited by CertiK" (found), "audited by Trail of Bits" (not found)
        # Score: 2/3
        self.assertAlmostEqual(eval_result['factual_accuracy'], 2/3, places=5)

    def test_evaluate_response_missing_ground_truth_keys(self):
        ai_response = MockAIResponseForEval(content="Test response", tone="neutral")
        evaluator = Evaluator()
        # No ground_truth_data for expected_tone
        eval_result_no_tone_gt = evaluator.evaluate_response(cast(AIResponse, ai_response), ground_truth_data={})
        self.assertEqual(eval_result_no_tone_gt['tone_match'], "N/A (no 'expected_tone' in ground_truth_data)")
        # factual_accuracy will run with None facts, returning 1.0
        self.assertEqual(eval_result_no_tone_gt['factual_accuracy'], 1.0)

        # No ground_truth_data at all for factual_accuracy
        eval_result_no_facts_gt = evaluator.evaluate_response(cast(AIResponse, ai_response), ground_truth_data=None)
        self.assertEqual(eval_result_no_facts_gt['factual_accuracy'], 1.0)

    def test_evaluate_response_missing_input_for_relevance(self):
        ai_response = MockAIResponseForEval(content="Test response", tone="neutral")
        evaluator = Evaluator(metrics_to_run=['relevance'])
        eval_result = evaluator.evaluate_response(cast(AIResponse, ai_response), original_tweet_content=None)
        self.assertEqual(eval_result['relevance'], "N/A (no 'original_tweet_content' provided for relevance)")

    def test_evaluate_response_airesponse_missing_attributes(self):
        # Test case: AIResponse is missing the 'tone' attribute
        class AIResponseNoTone:
            def __init__(self, content: str):
                self.content = content
        
        ai_response_no_tone = AIResponseNoTone(content="Some text content")
        evaluator = Evaluator(metrics_to_run=['tone_match'])
        eval_result = evaluator.evaluate_response(cast(AIResponse, ai_response_no_tone), ground_truth_data={"expected_tone": "positive"})
        self.assertEqual(eval_result['tone_match'], "Error: AIResponse object missing 'tone' attribute.")

        # Test case: AIResponse is missing the 'content' attribute for relevance
        class AIResponseNoContent:
            def __init__(self, tone: str):
                self.tone = tone

        ai_response_no_content = AIResponseNoContent(tone="positive")
        evaluator_relevance = Evaluator(metrics_to_run=['relevance'])
        eval_result_relevance = evaluator_relevance.evaluate_response(cast(AIResponse, ai_response_no_content), original_tweet_content="A question")
        self.assertEqual(eval_result_relevance['relevance'], "Error: AIResponse object missing 'content' attribute.")

    def test_run_batch_evaluation(self):
        if not self.golden_set_data or len(self.golden_set_data) < 2:
            self.skipTest("Golden set data not loaded or insufficient for batch test.")

        sample1_data = self.golden_set_data[0]
        ai_res1 = MockAIResponseForEval(sample1_data["ai_response_content"], sample1_data["ai_response_analyzed_tone"])
        
        sample2_data = self.golden_set_data[1]
        ai_res2 = MockAIResponseForEval(sample2_data["ai_response_content"], sample2_data["ai_response_analyzed_tone"])

        evaluation_batch = [
            (cast(AIResponse, ai_res1), sample1_data["original_tweet_content"], sample1_data.get("knowledge_snippet_used"), sample1_data["ground_truth_data"]),
            (cast(AIResponse, ai_res2), sample2_data["original_tweet_content"], sample2_data.get("knowledge_snippet_used"), sample2_data["ground_truth_data"])
        ]

        evaluator = Evaluator()
        batch_results = evaluator.run_batch_evaluation(evaluation_batch)
        self.assertEqual(len(batch_results), 2)
        self.assertIn('tone_match', batch_results[0])
        self.assertAlmostEqual(batch_results[0]['tone_match'], 1.0)
        self.assertAlmostEqual(batch_results[1]['tone_match'], 0.0)

if __name__ == '__main__':
    unittest.main() 