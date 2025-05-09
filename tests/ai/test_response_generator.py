# Changelog:
# 2025-05-07 HH:MM - Step 9 - Initial implementation of tests for ResponseGenerator.

import unittest
from unittest.mock import patch, MagicMock, ANY
import os
import sys

# Ensure the test can find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai.response_generator import generate_tweet_reply, generate_new_tweet # type: ignore
from src.models.tweet import Tweet, TweetMetadata # type: ignore
from src.models.account import Account, AccountType # type: ignore
from src.models.response import AIResponse, ResponseType # type: ignore
from src.ai.xai_client import APIError as XAIAPIError # type: ignore

# Dummy Account and Tweet instances for testing
OFFICIAL_ACCOUNT = Account(
    account_id="official_yieldfi", username="YieldFiOfficial", account_type=AccountType.OFFICIAL,
    display_name="YieldFi Official", platform="Twitter", follower_count=10000
)
INTERN_ACCOUNT = Account(
    account_id="intern_yieldfi", username="YieldFiIntern", account_type=AccountType.INTERN,
    display_name="YieldFi Intern", platform="Twitter", follower_count=100
)
TARGET_ACCOUNT_INSTITUTION = Account(
    account_id="bigbankinc", username="BigBankInc", account_type=AccountType.INSTITUTION,
    display_name="Big Bank Inc", platform="Twitter", follower_count=500000
)
ORIGINAL_TWEET_NEUTRAL = Tweet(
    content="What is YieldFi?",
    metadata=TweetMetadata(tweet_id="orig001", created_at="2024-01-01T00:00:00Z", author_id="user01", author_username="curiousUser")
)
ORIGINAL_TWEET_NEGATIVE = Tweet(
    content="I am having issues with YieldFi staking. It is frustrating!",
    metadata=TweetMetadata(tweet_id="orig002", created_at="2024-01-02T00:00:00Z", author_id="user02", author_username="frustratedUser"),
    tone="negative", sentiment_score=-0.7
)

class TestResponseGenerator(unittest.TestCase):

    @patch('src.ai.response_generator.XAIClient')
    @patch('src.ai.response_generator.generate_interaction_prompt')
    @patch('src.ai.response_generator.analyze_tweet_tone')
    @patch('src.ai.response_generator.MockKnowledgeRetriever')
    def test_generate_tweet_reply_success(self, MockKnowledge, mock_analyze_tone, mock_gen_prompt, MockXAI):
        # Setup Mocks
        mock_analyze_tone.return_value = ORIGINAL_TWEET_NEUTRAL # Assume tone is analyzed
        mock_gen_prompt.return_value = "<Generated Interaction Prompt>"
        
        mock_xai_instance = MockXAI.return_value
        mock_xai_instance.get_completion.return_value = {"choices": [{"text": "AI Reply Content"}]}

        mock_knowledge_instance = MockKnowledge.return_value
        mock_knowledge_instance.get_relevant_knowledge.return_value = "Mocked Knowledge Snippet"

        # Call function
        response = generate_tweet_reply(
            original_tweet=ORIGINAL_TWEET_NEUTRAL,
            responding_as=OFFICIAL_ACCOUNT,
            target_account=TARGET_ACCOUNT_INSTITUTION,
            knowledge_retriever=mock_knowledge_instance
        )

        # Assertions
        self.assertIsInstance(response, AIResponse)
        self.assertEqual(response.content, "AI Reply Content")
        self.assertEqual(response.response_type, ResponseType.TWEET_REPLY)
        mock_analyze_tone.assert_called_once_with(ORIGINAL_TWEET_NEUTRAL)
        mock_knowledge_instance.get_relevant_knowledge.assert_called_once_with(ORIGINAL_TWEET_NEUTRAL.content)
        mock_gen_prompt.assert_called_once_with(
            original_post_content=ORIGINAL_TWEET_NEUTRAL.content,
            active_account_info=OFFICIAL_ACCOUNT,
            target_account_info=TARGET_ACCOUNT_INSTITUTION,
            yieldfi_knowledge_snippet="Mocked Knowledge Snippet",
            interaction_details={},
            platform="Twitter"
        )
        mock_xai_instance.get_completion.assert_called_once_with(prompt="<Generated Interaction Prompt>", max_tokens=512)
        self.assertEqual(response.source_tweet_id, ORIGINAL_TWEET_NEUTRAL.metadata.tweet_id)

    @patch('src.ai.response_generator.XAIClient')
    @patch('src.ai.response_generator.generate_new_tweet_prompt')
    @patch('src.ai.response_generator.MockKnowledgeRetriever')
    def test_generate_new_tweet_success(self, MockKnowledge, mock_gen_new_prompt, MockXAI):
        # Setup Mocks
        mock_gen_new_prompt.return_value = "<Generated New Tweet Prompt>"
        mock_xai_instance = MockXAI.return_value
        mock_xai_instance.get_completion.return_value = {"choices": [{"text": "AI New Tweet Content"}]}

        mock_knowledge_instance = MockKnowledge.return_value
        mock_knowledge_instance.search_knowledge_for_topic.return_value = "Mocked Knowledge for New Tweet"

        # Call function
        response = generate_new_tweet(
            category="Product Update",
            responding_as=INTERN_ACCOUNT,
            topic="New Feature Launch!",
            knowledge_retriever=mock_knowledge_instance
        )

        # Assertions
        self.assertIsInstance(response, AIResponse)
        self.assertEqual(response.content, "AI New Tweet Content")
        self.assertEqual(response.response_type, ResponseType.NEW_TWEET)
        mock_knowledge_instance.search_knowledge_for_topic.assert_called_once_with("New Feature Launch!", "Product Update")
        mock_gen_new_prompt.assert_called_once_with(
            category="Product Update",
            topic="New Feature Launch!",
            active_account_info=INTERN_ACCOUNT,
            yieldfi_knowledge_snippet="Mocked Knowledge for New Tweet",
            platform="Twitter",
            additional_instructions=None
        )
        mock_xai_instance.get_completion.assert_called_once_with(prompt="<Generated New Tweet Prompt>", max_tokens=512)

    @patch('src.ai.response_generator.XAIClient')
    @patch('src.ai.response_generator.generate_interaction_prompt')
    @patch('src.ai.response_generator.analyze_tweet_tone')
    def test_generate_tweet_reply_xai_api_error(self, mock_analyze_tone, mock_gen_prompt, MockXAI):
        mock_analyze_tone.return_value = ORIGINAL_TWEET_NEGATIVE
        mock_gen_prompt.return_value = "<Prompt Causing Error>"
        mock_xai_instance = MockXAI.return_value
        mock_xai_instance.get_completion.side_effect = XAIAPIError("XAI Key Invalid", status_code=401)

        response = generate_tweet_reply(ORIGINAL_TWEET_NEGATIVE, OFFICIAL_ACCOUNT)

        self.assertIn("[Error: AI API call failed - XAI Key Invalid]", response.content)
        self.assertEqual(response.response_type, ResponseType.TWEET_REPLY)

    @patch('src.ai.response_generator.XAIClient') # Mock XAIClient to avoid its actual instantiation error
    @patch('src.ai.response_generator.generate_interaction_prompt', side_effect=ValueError("Prompt Gen Error"))
    @patch('src.ai.response_generator.analyze_tweet_tone')
    def test_generate_tweet_reply_prompt_generation_error(self, mock_analyze_tone, mock_gen_prompt, MockXAI):
        mock_analyze_tone.return_value = ORIGINAL_TWEET_NEUTRAL
        # XAIClient itself is mocked, so its constructor won't run into config issues for this test
        mock_xai_instance = MockXAI.return_value 
        
        response = generate_tweet_reply(ORIGINAL_TWEET_NEUTRAL, OFFICIAL_ACCOUNT)

        self.assertIn("[Error: Unexpected error during response generation - Prompt Gen Error]", response.content)

    # Test for alternative response structures (e.g., PaLM style)
    @patch('src.ai.response_generator.XAIClient')
    @patch('src.ai.response_generator.generate_interaction_prompt')
    @patch('src.ai.response_generator.analyze_tweet_tone')
    def test_generate_tweet_reply_palm_response_structure(self, mock_analyze_tone, mock_gen_prompt, MockXAI):
        mock_analyze_tone.return_value = ORIGINAL_TWEET_NEUTRAL
        mock_gen_prompt.return_value = "<Palm Prompt>"
        mock_xai_instance = MockXAI.return_value
        mock_xai_instance.get_completion.return_value = {"candidates": [{"output": "PaLM AI Reply"}]}

        response = generate_tweet_reply(ORIGINAL_TWEET_NEUTRAL, OFFICIAL_ACCOUNT)
        self.assertEqual(response.content, "PaLM AI Reply")

    @patch('src.ai.response_generator.XAIClient')
    @patch('src.ai.response_generator.generate_interaction_prompt')
    @patch('src.ai.response_generator.analyze_tweet_tone')
    def test_generate_tweet_reply_unclear_response_structure(self, mock_analyze_tone, mock_gen_prompt, MockXAI):
        mock_analyze_tone.return_value = ORIGINAL_TWEET_NEUTRAL
        mock_gen_prompt.return_value = "<Unclear Prompt>"
        mock_xai_instance = MockXAI.return_value
        mock_xai_instance.get_completion.return_value = {"some_other_key": "some_value"} # No choices or candidates

        response = generate_tweet_reply(ORIGINAL_TWEET_NEUTRAL, OFFICIAL_ACCOUNT)
        self.assertIn("[Warning: AI response structure not recognized]", response.content)

if __name__ == '__main__':
    unittest.main() 