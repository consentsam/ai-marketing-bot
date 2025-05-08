# Changelog:
# - 2025-05-17: Corrected expected value for relevance score test case 1.
# - 2025-05-16: Initial creation for Step 21 (Evaluation Framework).
#   - Added unit tests for calculate_tone_match_score, calculate_relevance_score, calculate_factual_accuracy_score.

import unittest
from typing import Set, Optional, List

# Ensure NLTK is available for _preprocess_text, or mock it if tests are strictly isolated.
# For these tests, we assume NLTK is installed and resources (stopwords, punkt) are available.
try:
    from src.evaluation.metrics import (
        calculate_tone_match_score,
        calculate_relevance_score,
        calculate_factual_accuracy_score,
        _preprocess_text, # Also test the helper if it's complex enough
        DEFAULT_STOP_WORDS
    )
    NLTK_AVAILABLE_FOR_TEST = True
except ImportError:
    # Fallback for local execution if PYTHONPATH is not set
    NLTK_AVAILABLE_FOR_TEST = False
    # Define dummy functions if needed for tests to run without NLTK, though they might fail logically
    def calculate_tone_match_score(g,e): return 0.0
    def calculate_relevance_score(g,i,k=None,s=None): return 0.0
    def calculate_factual_accuracy_score(g,f=None): return 0.0
    def _preprocess_text(t, s): return set()
    DEFAULT_STOP_WORDS = set()
except LookupError:
    # If import succeeded but resources missing
    print("WARNING: NLTK imported but resources missing. Tests requiring NLTK will be skipped.")
    NLTK_AVAILABLE_FOR_TEST = False
    # Define dummy functions
    def calculate_tone_match_score(g,e): return 0.0 # Keep non-NLTK tests runnable
    def calculate_relevance_score(g,i,k=None,s=None): return 0.0
    def calculate_factual_accuracy_score(g,f=None): return 1.0 # Keep non-NLTK tests runnable
    def _preprocess_text(t, s): return set()
    DEFAULT_STOP_WORDS = set()

@unittest.skipUnless(NLTK_AVAILABLE_FOR_TEST, "Skipping NLTK-dependent tests: NLTK resources not found.")
class TestEvaluationMetricsNLTK(unittest.TestCase):
    """Tests requiring NLTK resources."""
    def test_preprocess_text(self):
        custom_stopwords: Set[str] = {"is", "a", "the"}.union(DEFAULT_STOP_WORDS)
        self.assertEqual(_preprocess_text("This is a Sample Text!", custom_stopwords), {"sample", "text"})
        self.assertEqual(_preprocess_text("Another one, with numbers 123.", custom_stopwords), {"another", "one", "numbers", "123"})
        self.assertEqual(_preprocess_text("", custom_stopwords), set())
        self.assertEqual(_preprocess_text("Stopwords only is the an", custom_stopwords), set())
        self.assertTrue("product" in _preprocess_text("This product is great", DEFAULT_STOP_WORDS))
        self.assertFalse("is" in _preprocess_text("This product is great", DEFAULT_STOP_WORDS))

    def test_calculate_relevance_score(self):
        # Test case 1: Example from metrics.py __main__
        text_ex1 = "This is a great and awesome product with many features."
        context_ex1 = "The product is awesome and has great features."
        knowledge_ex1 = "It was released last year."
        # Expected: 4 / 9 = 0.444...
        self.assertAlmostEqual(calculate_relevance_score(text_ex1, context_ex1, knowledge_ex1), 4/9, places=3)

        # Test case 2: No overlap
        text2 = "The weather is sunny today."
        context2 = "What are the best cryptocurrencies to invest in?"
        self.assertAlmostEqual(calculate_relevance_score(text2, context2), 0.0, places=3)

        # Test case 3: Empty generated text
        self.assertAlmostEqual(calculate_relevance_score("", "Some valid context."), 0.0, places=3)

        # Test case 4: Empty context (and no knowledge)
        self.assertAlmostEqual(calculate_relevance_score("Some generated text.", ""), 0.0, places=3)
        
        # Test case 5: Both empty (after processing)
        self.assertAlmostEqual(calculate_relevance_score("is a the", "an the is of"), 1.0, places=3) # Both become empty sets
        self.assertAlmostEqual(calculate_relevance_score("", ""), 1.0, places=3) # Already empty

        # Test case 6: Perfect match (after processing)
        text6 = "YieldFi is great"
        context6 = "yieldfi IS great!"
        self.assertAlmostEqual(calculate_relevance_score(text6, context6), 1.0, places=3)
        
        # Test case 7: Context is subset of generated
        text7 = "Alpha beta gamma delta"
        context7 = "Alpha beta"
        # p_text7 = {alpha, beta, gamma, delta} (4)
        # p_context7 = {alpha, beta} (2)
        # Inter: {alpha, beta} (2). Union: {alpha, beta, gamma, delta} (4). Score: 2/4 = 0.5
        self.assertAlmostEqual(calculate_relevance_score(text7, context7), 0.5, places=3)

        # Test case 8: Generated is subset of context
        text8 = "Alpha beta"
        context8 = "Alpha beta gamma delta"
        self.assertAlmostEqual(calculate_relevance_score(text8, context8), 0.5, places=3)

# Tests that do NOT require NLTK resources
class TestEvaluationMetricsNoNLTK(unittest.TestCase):

    def test_calculate_tone_match_score(self):
        self.assertEqual(calculate_tone_match_score("positive", "positive"), 1.0)
        self.assertEqual(calculate_tone_match_score("Positive", "positive"), 1.0)
        self.assertEqual(calculate_tone_match_score("positive", "Positive"), 1.0)
        self.assertEqual(calculate_tone_match_score("positive", "negative"), 0.0)
        self.assertEqual(calculate_tone_match_score(None, "positive"), 0.0)
        self.assertEqual(calculate_tone_match_score("positive", None), 0.0)
        self.assertEqual(calculate_tone_match_score(None, None), 0.0)
        self.assertEqual(calculate_tone_match_score("", "positive"), 0.0)
        self.assertEqual(calculate_tone_match_score("positive", ""), 0.0)
        self.assertEqual(calculate_tone_match_score("", ""), 0.0)

    def test_calculate_factual_accuracy_score(self):
        text = "YieldFi was founded in 2023. It offers high APY. The CEO is Satoshi."
        
        # All facts present
        facts1 = ["founded in 2023", "high APY", "CEO is Satoshi"]
        self.assertEqual(calculate_factual_accuracy_score(text, facts1), 1.0)

        # Some facts present
        facts2 = ["founded in 2023", "low APY"]
        self.assertEqual(calculate_factual_accuracy_score(text, facts2), 0.5) # 1 out of 2

        # No facts present
        facts3 = ["audited by XYZ", "based in London"]
        self.assertEqual(calculate_factual_accuracy_score(text, facts3), 0.0)

        # Empty list of facts (vacuously true)
        facts4: List[str] = []
        self.assertEqual(calculate_factual_accuracy_score(text, facts4), 1.0)

        # None for facts (vacuously true)
        self.assertEqual(calculate_factual_accuracy_score(text, None), 1.0)

        # Case sensitivity of facts (should be case-insensitive due to .lower() in metric)
        facts5 = ["FOUNDED IN 2023", "ceo is SATOSHI"]
        self.assertEqual(calculate_factual_accuracy_score(text, facts5), 1.0)

        # Fact with leading/trailing spaces
        facts6 = [" founded in 2023 "]
        self.assertEqual(calculate_factual_accuracy_score(text, facts6), 1.0)
        
        # Empty text, but facts to check
        facts7 = ["fact1"]
        self.assertEqual(calculate_factual_accuracy_score("", facts7), 0.0)

if __name__ == '__main__':
    # This allows running tests directly, but pytest is preferred
    # It will run all tests if NLTK resources are available
    if not NLTK_AVAILABLE_FOR_TEST:
        print("WARNING: NLTK resources missing, only running non-NLTK tests.")
        suite = unittest.TestSuite()
        suite.addTest(unittest.makeSuite(TestEvaluationMetricsNoNLTK))
        runner = unittest.TextTestRunner()
        runner.run(suite)
    else:
        unittest.main() 