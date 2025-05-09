# Changelog:
# 2025-05-19 13:00 - Step 25 - Created tests for interaction modes functionality.
# 2025-05-19 13:15 - Step 25 - Simplified test approach for interaction modes.
# 2025-05-19 13:25 - Step 25 - Fixed failing test for get_base_yieldfi_persona_accepts_mode.

import os
import sys
import unittest
from unittest import mock

# Ensure the test can find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai.prompt_engineering import (
    get_base_yieldfi_persona,
    generate_interaction_prompt,
    generate_new_tweet_prompt,
    InteractionMode
)
from src.models.account import Account, AccountType
from src.models.category import TweetCategory
from src.ai.response_generator import generate_tweet_reply, generate_new_tweet

# Mock the logger to avoid logging during tests
@mock.patch('src.ai.prompt_engineering.logger')
class TestInteractionModes(unittest.TestCase):
    
    def setUp(self):
        # Create test account for reuse
        self.test_account = Account(
            account_id="test", 
            username="test_user", 
            display_name="Test User", 
            account_type=AccountType.OFFICIAL
        )
        
        # Create test category for reuse
        self.test_category = TweetCategory(
            name="Announcement",
            description="Important updates about YieldFi",
            prompt_keywords=["launch", "update"],
            style_guidelines={"tone": "Informative"}
        )
        
        # Test content for prompt generation
        self.test_content = "Hello, what are the latest updates from YieldFi?"
    
    def test_get_base_yieldfi_persona_accepts_mode(self, mock_logger):
        """Test that get_base_yieldfi_persona accepts a mode parameter"""
        # This mostly verifies the function signature was updated correctly
        with mock.patch('src.ai.prompt_engineering.load_mode_instructions', return_value="""
        # TestMode Mode Instructions
        
        ## Tone Guidelines
        - Test tone guideline 1
        - Test tone guideline 2
        """):
            # Default mode
            default_persona = get_base_yieldfi_persona(AccountType.OFFICIAL, "Default")
            self.assertIn("official voice of YieldFi", default_persona)
            
            # Other mode (should call load_mode_instructions)
            other_persona = get_base_yieldfi_persona(AccountType.OFFICIAL, "TestMode")
            self.assertIn("official voice of YieldFi", other_persona)
            self.assertIn("mode-specific guidelines", other_persona.lower())
            self.assertIn("test tone guideline", other_persona.lower())
    
    def test_generate_interaction_prompt_accepts_mode(self, mock_logger):
        """Test that generate_interaction_prompt accepts and uses a mode parameter"""
        with mock.patch('src.ai.prompt_engineering.get_base_yieldfi_persona') as mock_persona:
            mock_persona.return_value = "Test persona with mode"
            
            # Call with mode parameter
            generate_interaction_prompt(
                original_post_content=self.test_content,
                active_account_info=self.test_account,
                mode="TestMode"
            )
            
            # Verify mode was passed to get_base_yieldfi_persona
            mock_persona.assert_called_with(AccountType.OFFICIAL, "TestMode")
    
    def test_generate_new_tweet_prompt_accepts_mode(self, mock_logger):
        """Test that generate_new_tweet_prompt accepts and uses a mode parameter"""
        with mock.patch('src.ai.prompt_engineering.get_base_yieldfi_persona') as mock_persona:
            mock_persona.return_value = "Test persona with mode"
            
            # Call with mode parameter
            generate_new_tweet_prompt(
                category=self.test_category,
                active_account_info=self.test_account,
                topic="Test topic",
                mode="TestMode"
            )
            
            # Verify mode was passed to get_base_yieldfi_persona
            mock_persona.assert_called_with(AccountType.OFFICIAL, "TestMode")
    
    @mock.patch('src.ai.response_generator.XAIClient')
    @mock.patch('src.ai.response_generator.generate_interaction_prompt')
    def test_response_generator_passes_mode(self, mock_prompt, mock_xai_client, mock_logger):
        """Test that generate_tweet_reply passes the mode parameter to generate_interaction_prompt"""
        # Setup mock AI client
        mock_instance = mock_xai_client.return_value
        mock_instance.xai_model = "test-model"
        mock_instance.get_completion.return_value = {
            "choices": [{"text": "Mock AI response"}]
        }
        
        # Setup mock prompt function
        mock_prompt.return_value = "Test prompt"
        
        # Create test tweet
        from src.models.tweet import Tweet, TweetMetadata
        test_tweet = Tweet(
            content="Test tweet",
            metadata=TweetMetadata(
                tweet_id="123",
                created_at="2023-01-01T12:00:00Z",
                author_id="456",
                author_username="test_author"
            )
        )
        
        # Test with mode parameter
        generate_tweet_reply(
            original_tweet=test_tweet,
            responding_as=self.test_account,
            interaction_mode="TestMode"
        )
        
        # Verify mode was passed to generate_interaction_prompt
        self.assertTrue(mock_prompt.called)
        # Get the call args as dict
        call_kwargs = mock_prompt.call_args[1]
        self.assertEqual(call_kwargs['mode'], "TestMode")
    
    @mock.patch('src.ai.response_generator.XAIClient')
    @mock.patch('src.ai.response_generator.generate_new_tweet_prompt')
    def test_new_tweet_generator_passes_mode(self, mock_prompt, mock_xai_client, mock_logger):
        """Test that generate_new_tweet passes the mode parameter to generate_new_tweet_prompt"""
        # Setup mock AI client
        mock_instance = mock_xai_client.return_value
        mock_instance.xai_model = "test-model"
        mock_instance.get_completion.return_value = {
            "choices": [{"text": "Mock AI response"}]
        }
        
        # Setup mock prompt function
        mock_prompt.return_value = "Test prompt"
        
        # Test with mode parameter
        generate_new_tweet(
            category=self.test_category,
            responding_as=self.test_account,
            topic="Test topic",
            interaction_mode="TestMode"
        )
        
        # Verify mode was passed to generate_new_tweet_prompt
        self.assertTrue(mock_prompt.called)
        # Get the call args as dict
        call_kwargs = mock_prompt.call_args[1]
        self.assertEqual(call_kwargs['mode'], "TestMode")


if __name__ == "__main__":
    unittest.main() 