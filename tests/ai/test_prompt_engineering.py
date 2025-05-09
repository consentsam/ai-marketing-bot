# Changelog:
# 2025-05-07 HH:MM - Step 20 (Initial) - Added comprehensive tests for prompt engineering.

import unittest
from unittest.mock import MagicMock
import os

# Ensure the test can find the src modules
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai.prompt_engineering import (
    get_base_yieldfi_persona,
    get_instruction_set,
    generate_interaction_prompt,
    generate_new_tweet_prompt,
    YIELDFI_CORE_MESSAGE
) # type: ignore
from src.models.account import Account, AccountType # type: ignore

class TestPromptEngineering(unittest.TestCase):

    def setUp(self):
        self.official_account = Account(
            account_id="official_id", username="YieldFiOfficial", display_name="YieldFi Official",
            account_type=AccountType.OFFICIAL, platform="Twitter", follower_count=10000, bio="Official YieldFi Account"
        )
        self.intern_account = Account(
            account_id="intern_id", username="YieldFiIntern", display_name="YieldFi Intern",
            account_type=AccountType.INTERN, platform="Twitter", follower_count=100, bio="YieldFi Intern here to help!"
        )
        self.partner_account = Account(
            account_id="partner_id", username="PartnerCo", display_name="Partner Company",
            account_type=AccountType.PARTNER, platform="Twitter", follower_count=5000, bio="Proud Partner of YieldFi"
        )
        self.institution_account = Account(
            account_id="inst_id", username="BigInstitution", display_name="Big Institution",
            account_type=AccountType.INSTITUTION, platform="Twitter", follower_count=100000, bio="Financial Institution"
        )
        self.unknown_account = Account(
            account_id="unknown_id", username="User123", display_name="Random User",
            account_type=AccountType.UNKNOWN, platform="Twitter", follower_count=50, bio="Just a user"
        )

    def test_get_base_yieldfi_persona(self):
        self.assertIn("official voice of yieldfi", get_base_yieldfi_persona(AccountType.OFFICIAL).lower())
        self.assertIn("yieldfi intern", get_base_yieldfi_persona(AccountType.INTERN).lower())
        self.assertIn("yieldfi partner", get_base_yieldfi_persona(AccountType.PARTNER).lower())
        # For other types, a generic persona is returned
        self.assertIn("representative of yieldfi", get_base_yieldfi_persona(AccountType.INSTITUTION).lower())
        self.assertIn("representative of yieldfi", get_base_yieldfi_persona(AccountType.UNKNOWN).lower())

    def test_get_instruction_set(self):
        # Test specific pairings
        official_to_institution_instructions = get_instruction_set(AccountType.OFFICIAL, AccountType.INSTITUTION).lower()
        self.assertIn("responding to institutions", official_to_institution_instructions)
        self.assertIn("highly professional tone", official_to_institution_instructions)

        official_to_partner_instructions = get_instruction_set(AccountType.OFFICIAL, AccountType.PARTNER).lower()
        self.assertIn("engaging with partners", official_to_partner_instructions)
        self.assertIn("collaborative and appreciative tone", official_to_partner_instructions)
        
        intern_to_intern_instructions = get_instruction_set(AccountType.INTERN, AccountType.INTERN).lower()
        self.assertIn("interacting with other interns", intern_to_intern_instructions)
        self.assertIn("friendly, supportive, and relatable", intern_to_intern_instructions)

        # Test a default/fallback case
        official_to_unknown_instructions = get_instruction_set(AccountType.OFFICIAL, AccountType.UNKNOWN).lower()
        self.assertIn("tailor your response to the context", official_to_unknown_instructions)
        self.assertIn("maintain yieldfi's brand voice", official_to_unknown_instructions)

    def test_generate_interaction_prompt_official_to_institution(self):
        prompt = generate_interaction_prompt(
            original_post_content="Tell me about YieldFi security.",
            active_account_info=self.official_account,
            target_account_info=self.institution_account,
            yieldfi_knowledge_snippet="YieldFi uses multi-layer security protocols."
        )
        self.assertIn(get_base_yieldfi_persona(AccountType.OFFICIAL), prompt)
        self.assertIn(YIELDFI_CORE_MESSAGE.strip(), prompt)
        self.assertIn("Original Post to Reply To: \"Tell me about YieldFi security.\"", prompt)
        self.assertIn(f"Target Account: @{self.institution_account.username}", prompt)
        self.assertIn(get_instruction_set(AccountType.OFFICIAL, AccountType.INSTITUTION).strip(), prompt)
        self.assertIn("Relevant YieldFi Knowledge: YieldFi uses multi-layer security protocols.", prompt)
        self.assertIn("Task: Craft a response", prompt)
        self.assertIn("Keep the response under 280 characters", prompt) # Default platform Twitter
        self.assertIn("CRITICAL INSTRUCTIONS:", prompt)
        self.assertTrue(prompt.strip().endswith("Response:") or prompt.strip().endswith("Tweet:"))

    def test_generate_interaction_prompt_intern_to_intern(self):
        prompt = generate_interaction_prompt(
            original_post_content="Cool new feature!",
            active_account_info=self.intern_account,
            target_account_info=self.intern_account,
            interaction_details={'tone': 'excited', 'goal': 'share enthusiasm'}
        )
        self.assertIn(get_base_yieldfi_persona(AccountType.INTERN), prompt)
        self.assertIn(get_instruction_set(AccountType.INTERN, AccountType.INTERN).strip(), prompt)
        self.assertIn("Use a excited tone.", prompt)
        self.assertIn("Goal: share enthusiasm.", prompt)
        self.assertNotIn("Relevant YieldFi Knowledge:", prompt)
        self.assertIn("CRITICAL INSTRUCTIONS:", prompt)
        self.assertTrue(prompt.strip().endswith("Response:") or prompt.strip().endswith("Tweet:"))

    def test_generate_interaction_prompt_minimal_input(self):
        # Only active account, no original post, no target, no knowledge, no details
        prompt = generate_interaction_prompt(
            original_post_content=None,
            active_account_info=self.official_account
        )
        self.assertIn(get_base_yieldfi_persona(AccountType.OFFICIAL), prompt)
        self.assertIn(YIELDFI_CORE_MESSAGE.strip(), prompt)
        self.assertNotIn("Original Post to Reply To:", prompt)
        self.assertNotIn("Target Account:", prompt)
        self.assertNotIn("Interaction Instructions:", prompt) # No target, so no specific instruction set
        self.assertNotIn("Relevant YieldFi Knowledge:", prompt)
        self.assertIn("Goal: engage and inform.", prompt) # Default goal
        self.assertIn("CRITICAL INSTRUCTIONS:", prompt)
        self.assertTrue(prompt.strip().endswith("Response:") or prompt.strip().endswith("Tweet:"))

    def test_generate_interaction_prompt_non_twitter_platform(self):
        prompt = generate_interaction_prompt(
            original_post_content="Hello",
            active_account_info=self.official_account,
            platform="Discord"
        )
        self.assertNotIn("Keep the response under 280 characters", prompt)
        # We could add a check for Discord specific instructions if they existed in the function

    def test_generate_new_tweet_prompt_with_topic_and_knowledge(self):
        prompt = generate_new_tweet_prompt(
            category="Product Update",
            topic="New Staking Options Available!",
            yieldfi_knowledge_snippet="Earn up to 20% APY on new ETH staking.",
            active_account_info=self.official_account
        )
        self.assertIn(get_base_yieldfi_persona(AccountType.OFFICIAL), prompt)
        self.assertIn(YIELDFI_CORE_MESSAGE.strip(), prompt)
        self.assertIn("Tweet Category: Product Update", prompt)
        self.assertIn("Specific Topic: New Staking Options Available!", prompt)
        self.assertIn("Relevant YieldFi Knowledge: Earn up to 20% APY on new ETH staking.", prompt)
        self.assertIn("Task: Create a new tweet", prompt)
        self.assertIn("Keep the tweet under 280 characters", prompt) # Default platform Twitter
        self.assertIn("CRITICAL INSTRUCTIONS:", prompt)
        self.assertTrue(prompt.strip().endswith("Tweet:"))

    def test_generate_new_tweet_prompt_minimal_category_only(self):
        prompt = generate_new_tweet_prompt(
            category="Community Update",
            active_account_info=self.intern_account # Test with intern
        )
        self.assertIn(get_base_yieldfi_persona(AccountType.INTERN), prompt)
        self.assertIn("Tweet Category: Community Update", prompt)
        self.assertNotIn("Specific Topic:", prompt)
        self.assertNotIn("Relevant YieldFi Knowledge:", prompt)
        self.assertIn("CRITICAL INSTRUCTIONS:", prompt)
        self.assertTrue(prompt.strip().endswith("Tweet:"))
        
    def test_generate_new_tweet_prompt_default_persona_if_no_account(self):
        prompt = generate_new_tweet_prompt(
            category="Announcement"
        )
        # Should default to OFFICIAL persona
        self.assertIn(get_base_yieldfi_persona(AccountType.OFFICIAL), prompt)
        self.assertIn("Tweet Category: Announcement", prompt)
        self.assertIn("CRITICAL INSTRUCTIONS:", prompt)
        self.assertTrue(prompt.strip().endswith("Tweet:"))

if __name__ == '__main__':
    unittest.main() 