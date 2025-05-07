# Changelog:
# 2025-05-07 HH:MM - Step 8 - Initial implementation of tests for tone_analyzer.py

import unittest
from unittest.mock import patch, MagicMock
import os
import sys

# Ensure the test can find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai.tone_analyzer import _analyze_with_textblob, analyze_tone, analyze_tweet_tone # type: ignore
from src.models.tweet import Tweet, TweetMetadata # type: ignore
from src.models.account import Account, AccountType # type: ignore

class TestToneAnalyzer(unittest.TestCase):

    def test_analyze_with_textblob_positive(self):
        result = _analyze_with_textblob("YieldFi is great and I love it!")
        self.assertEqual(result['tone'], 'positive')
        self.assertGreater(result['sentiment_score'], 0.1)
        # Confidence is abs(polarity) or 1.0 for neutral
        self.assertEqual(result['confidence'], abs(result['sentiment_score'])) 

    def test_analyze_with_textblob_negative(self):
        result = _analyze_with_textblob("YieldFi is terrible and I hate it.")
        self.assertEqual(result['tone'], 'negative')
        self.assertLess(result['sentiment_score'], -0.1)
        self.assertEqual(result['confidence'], abs(result['sentiment_score']))

    def test_analyze_with_textblob_neutral(self):
        result = _analyze_with_textblob("YieldFi is a company.")
        self.assertEqual(result['tone'], 'neutral')
        self.assertAlmostEqual(result['sentiment_score'], 0.0, delta=0.1)
        self.assertEqual(result['confidence'], 1.0) # For neutral, confidence is 1.0

    def test_analyze_with_textblob_empty_string(self):
        result = _analyze_with_textblob("")
        self.assertEqual(result['tone'], 'neutral')
        self.assertEqual(result['sentiment_score'], 0.0)
        self.assertEqual(result['subjectivity'], 0.0)
        self.assertEqual(result['confidence'], 1.0)

    @patch('src.ai.tone_analyzer.get_config')
    def test_analyze_tone_default_method_textblob(self, mock_get_config):
        mock_get_config.return_value = 'textblob'
        result = analyze_tone("This is a test.")
        self.assertEqual(result['tone'], 'neutral') # "This is a test." is neutral by TextBlob
        mock_get_config.assert_called_once_with("tone_analysis.method", "textblob")

    @patch('src.ai.tone_analyzer.get_config')
    def test_analyze_tone_explicit_method_textblob(self, mock_get_config):
        result = analyze_tone("This is a positive test!", method="textblob")
        self.assertEqual(result['tone'], 'positive')
        # get_config should not be called if method is specified
        mock_get_config.assert_not_called()

    def test_analyze_tone_xai_not_implemented(self):
        with self.assertRaisesRegex(NotImplementedError, "xAI analysis method is not yet implemented."):
            analyze_tone("Test text", method="xai")

    def test_analyze_tone_google_palm_not_implemented(self):
        with self.assertRaisesRegex(NotImplementedError, "Google PaLM analysis method is not yet implemented."):
            analyze_tone("Test text", method="google_palm")

    @patch('src.ai.tone_analyzer.get_config')
    def test_analyze_tone_unknown_method_falls_back_to_textblob(self, mock_get_config):
        mock_get_config.return_value = 'textblob' # Fallback if get_config is called
        # We also check the print warning in the actual function, 
        # but here we verify it uses textblob's logic.
        with patch('builtins.print') as mock_print: # to suppress/check warning
            result = analyze_tone("This is a test using an unknown method.", method="unknown_method")
            self.assertEqual(result['tone'], 'neutral')
            mock_print.assert_any_call("Warning: Analysis method 'unknown_method' not found. Defaulting to 'textblob'.")
        # get_config should not be called if method is specified, even if unknown, as _get_analysis_method handles the default directly
        # The internal _get_analysis_method directly uses textblob if method is not in its map.
        mock_get_config.assert_not_called() 

    def test_analyze_tweet_tone(self):
        sample_tweet = Tweet(
            content="YieldFi's new update is groundbreaking and exciting!",
            metadata=TweetMetadata(tweet_id="t1", created_at="2025-01-01T00:00:00Z", author_id="a1", author_username="testuser")
        )
        updated_tweet = analyze_tweet_tone(sample_tweet)
        self.assertEqual(updated_tweet.tone, 'positive')
        self.assertGreater(updated_tweet.sentiment_score, 0.1)

    def test_analyze_tweet_tone_with_method_override(self):
        sample_tweet = Tweet(
            content="This is a test with method override.",
            metadata=TweetMetadata(tweet_id="t3", created_at="2025-01-01T00:00:00Z", author_id="a3", author_username="testuser3")
        )
        # This will raise NotImplementedError because 'xai' is not implemented
        with self.assertRaisesRegex(NotImplementedError, "xAI analysis method is not yet implemented."):
            analyze_tweet_tone(sample_tweet, method="xai")

if __name__ == '__main__':
    unittest.main() 