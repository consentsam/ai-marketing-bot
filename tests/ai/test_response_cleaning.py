import unittest
import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.ai.response_generator import _clean_response, _ensure_tweet_length, degen_partials

class TestResponseCleaning(unittest.TestCase):

    def test_empty_response(self):
        """Test that empty input returns empty output."""
        self.assertEqual(_clean_response(""), "")
        self.assertEqual(_clean_response(None), "")
    
    def test_clean_response_with_quote_marks(self):
        """Test extraction of content in quotes."""
        # Test with double quotes
        input_text_double = 'Some reasoning. "This is a perfect tweet, exactly 100 characters long, which is good for testing the quote extraction logic!" More reasoning.'
        expected_double = "This is a perfect tweet, exactly 100 characters long, which is good for testing the quote extraction logic!"
        self.assertEqual(_clean_response(input_text_double), expected_double)
        
        # Test with single quotes
        input_text_single = "Some text before. 'This is another great tweet example, also 100 characters long, perfect for this specific test case!!' Some text after."
        expected_single = "This is another great tweet example, also 100 characters long, perfect for this specific test case!!"
        self.assertEqual(_clean_response(input_text_single), expected_single)
        
        # Test multiline quoted tweet with escaped quotes inside
        input_text_multiline_double = '''
        Reasoning paragraph one.
        "This is a tweet that spans\nmultiple lines and has escaped \\"double quotes\\" and \\'single quotes\\' inside.\nIt should be extracted correctly."
        Reasoning paragraph two.
        '''
        expected_multiline_double = "This is a tweet that spans\nmultiple lines and has escaped \"double quotes\" and 'single quotes' inside.\nIt should be extracted correctly."
        self.assertEqual(_clean_response(input_text_multiline_double), expected_multiline_double)

        input_text_multiline_single = '''
        Some other reasoning.
        'This is a single-quoted tweet that also spans\nmultiple lines and contains an escaped \\'apostrophe\\' and \\"double quote\\" inside.\nThis must also work.'
        More text.
        '''
        expected_multiline_single = "This is a single-quoted tweet that also spans\nmultiple lines and contains an escaped 'apostrophe' and \"double quote\" inside.\nThis must also work."
        self.assertEqual(_clean_response(input_text_multiline_single), expected_multiline_single)
    
    def test_clean_response_with_response_label(self):
        """Test extraction after 'Response:' label."""
        input_text = "Response: This is the tweet after the label, it is a good length for a test tweet, clearly over 15 characters."
        expected = "This is the tweet after the label, it is a good length for a test tweet, clearly over 15 characters."
        self.assertEqual(_clean_response(input_text), expected)
    
    def test_clean_response_with_tweet_label(self):
        """Test extraction after 'Tweet:' label."""
        input_text = "Tweet: This is the content for the tweet. It is specific and long enough for the test case here."
        expected = "This is the content for the tweet. It is specific and long enough for the test case here."
        self.assertEqual(_clean_response(input_text), expected)
    
    def test_clean_response_with_reasoning_and_quotes_then_label(self):
        """Test filtering out reasoning paragraphs."""
        input_text = '''
I'm considering how to respond.
"This is the quoted tweet, it's specific and a good length."
Response: This would be incorrect if quote logic is right.
        '''
        expected = "This is the quoted tweet, it's specific and a good length."
        self.assertEqual(_clean_response(input_text), expected)
    
    def test_clean_response_with_final_version_label(self):
        """Test extraction after 'Final version:' label."""
        input_text = 'Final version: This is the final version of the tweet, it is over fifteen characters long for sure.'
        expected = "This is the final version of the tweet, it is over fifteen characters long for sure."
        self.assertEqual(_clean_response(input_text), expected)
    
    def test_long_response_truncation_via_ensure_length(self):
        """Test that long responses are properly truncated."""
        long_text = "This is a very long tweet that will exceed the character limit by a significant margin, so we need to make sure it gets truncated properly. " * 20
        result = _ensure_tweet_length(long_text)
        self.assertTrue(len(result) <= 280, f"Result too long: {len(result)}")
        self.assertTrue(result.endswith("..."), f"Result does not end with ...: {result}")
    
    def test_long_response_cleaning_fallback_empty(self):
        """Test when _clean_response has no better option than to truncate the whole input."""
        # This long text has no markers, and the final fallback in _clean_response should not pick it up.
        long_text_no_markers = "This is a very long text block without any clear tweet markers or paragraph structure that would indicate a tweet. It just keeps going and going and is definitely not a short direct answer. " * 20
        result = _clean_response(long_text_no_markers)
        self.assertEqual(result, "", f"Expected empty from long unmarked text, got: '{result}'")
    
    def test_problematic_response_paragraph_extraction(self):
        """Test handling of model responses with internal dialogue."""
        complex_input = """
I need to respond to this tweet about Bitcoin surpassing Amazon.
My goal is to connect this to YieldFi's offerings. This is just some reasoning text.

Exciting news about #Bitcoin! At YieldFi, we help you maximize returns on your crypto assets with secure staking and yield farming. #DeFi. This is the tweet.

Some more thoughts here at the end but they are not the tweet.
"""
        extracted = _clean_response(complex_input)
        expected_content = "Exciting news about #Bitcoin! At YieldFi, we help you maximize returns on your crypto assets with secure staking and yield farming. #DeFi. This is the tweet."
        self.assertEqual(extracted, expected_content)
        self.assertTrue(15 <= len(extracted) <= 280)

    def test_ensure_tweet_length(self):
        """Test the tweet length enforcement function."""
        short_tweet = "This is a short tweet, well over ten characters."
        self.assertEqual(_ensure_tweet_length(short_tweet), short_tweet)
        
        exact_length_tweet = "a" * 280
        self.assertEqual(_ensure_tweet_length(exact_length_tweet), exact_length_tweet)
        
        long_tweet = "a" * 300
        truncated = _ensure_tweet_length(long_tweet)
        self.assertTrue(len(truncated) <= 280)
        self.assertTrue(truncated.endswith("..."))
        
        sentence = "This is a very long sentence that will be truncated at a word boundary if possible, otherwise it will just be cut. " * 10
        truncated = _ensure_tweet_length(sentence)
        self.assertTrue(len(truncated) <= 280)
        self.assertTrue(truncated.endswith("..."))
        self.assertNotRegex(truncated, r'\s\.\.\.$')

    def test_degen_partials(self):
        """Test known Degen mode partial responses."""
        self.assertEqual(_clean_response("s milestone to yieldfi"), degen_partials["s milestone to yieldfi"])
        self.assertEqual(_clean_response("  S MILESTONE TO YIELDFI  "), degen_partials["s milestone to yieldfi"])
        self.assertEqual(_clean_response("s pump it now boys"), degen_partials["s pump it"])
        self.assertEqual(_clean_response("s to the moon!!!"), degen_partials["s to the moon"])

    def test_very_short_cleaned_response(self):
        """Test that very short, non-degen responses are returned as empty."""
        self.assertEqual(_clean_response("abcde"), "") # Less than 10 chars, not a degen key/value
        self.assertEqual(_clean_response("s short"), "") # Not a known degen partial and short
        self.assertEqual(_ensure_tweet_length("shorty"), "")
        # Ensure known degen values (even if short) pass _ensure_tweet_length
        self.assertEqual(_ensure_tweet_length(degen_partials["s pump it"]), degen_partials["s pump it"])

    def test_sentence_extraction_fallback_no_paragraphs(self):
        """Test the sentence extraction logic as a fallback."""
        # Case 1: Target sentence is middle, surrounded by clear reasoning markers
        input_text_sentences1 = "Instruction: This first part is reasoning. This is the second sentence and is the actual tweet content for this test, it's pretty good. My reasoning: This third sentence is also reasoning and should be ignored."
        expected1 = "This is the second sentence and is the actual tweet content for this test, it's pretty good."
        self.assertEqual(_clean_response(input_text_sentences1), expected1, f"Test 1 Extracted: '{_clean_response(input_text_sentences1)}'")

        # Case 2: Single long valid sentence
        input_text_single_long = "This single sentence is quite long but should be extracted as is because it is under the limit and is the only actual content here for this specific test, making it perfectly valid and not reasoning I think this is a tweet."
        self.assertEqual(_clean_response(input_text_single_long), input_text_single_long)

        # Case 3: Tweet is the first sentence
        input_text_tweet_first = "This is the actual tweet, short and sweet. My reasoning for this is that it is concise and to the point."
        expected_tweet_first = "This is the actual tweet, short and sweet."
        self.assertEqual(_clean_response(input_text_tweet_first), expected_tweet_first)

        # Case 4: Combine last two non-reasoning sentences
        input_combine = "My thought process is this. This is the first half of the tweet. This is the second half, also good and not reasoning."
        expected_combine = "This is the first half of the tweet. This is the second half, also good and not reasoning."
        self.assertEqual(_clean_response(input_combine), expected_combine, f"Test Combine Extracted: '{_clean_response(input_combine)}'")

        # Case 5: Only one valid sentence at the end
        input_last_valid = "Reasoning one. Reasoning two. This is the final tweet, perfectly valid."
        expected_last_valid = "This is the final tweet, perfectly valid."
        self.assertEqual(_clean_response(input_last_valid), expected_last_valid)

if __name__ == '__main__':
    unittest.main() 