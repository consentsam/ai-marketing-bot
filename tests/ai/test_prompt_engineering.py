# Changelog:
# 2025-05-08 00:00 - Step 20.3 - Updated tests to match current generate_interaction_prompt and generate_new_tweet_prompt implementations.

import unittest
from unittest.mock import MagicMock
import os
import sys

# Ensure the test can find the src modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai.prompt_engineering import (
    get_base_yieldfi_persona,
    get_instruction_set,
    generate_interaction_prompt,
    generate_new_tweet_prompt,
    YIELDFI_CORE_MESSAGE
)
from src.models.account import Account, AccountType
from src.models.tweet import Tweet, TweetMetadata
from src.models.category import TweetCategory

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
        self.institution_account = Account(
            account_id="inst_id", username="BigInstitution", display_name="Big Institution",
            account_type=AccountType.INSTITUTION, platform="Twitter", follower_count=100000, bio="Financial Institution"
        )

    def test_get_base_yieldfi_persona(self):
        persona_official = get_base_yieldfi_persona(AccountType.OFFICIAL).lower()
        self.assertIn("official voice of yieldfi", persona_official)
        persona_intern = get_base_yieldfi_persona(AccountType.INTERN).lower()
        self.assertIn("yieldfi intern", persona_intern)
        persona_institution = get_base_yieldfi_persona(AccountType.INSTITUTION).lower()
        self.assertIn("professional, data-driven", persona_institution)

    def test_get_instruction_set(self):
        inst_inst = get_instruction_set(AccountType.OFFICIAL, AccountType.INSTITUTION)
        self.assertIn("institutional-grade security", inst_inst)
        inst_part = get_instruction_set(AccountType.OFFICIAL, AccountType.PARTNER)
        self.assertIn("mutual benefits", inst_part)
        inst_unknown = get_instruction_set(AccountType.INTERN, None)
        self.assertIn("Be friendly, helpful", inst_unknown)

    def test_generate_interaction_prompt_official_to_institution(self):
        metadata = TweetMetadata(author_username="UserX")
        tweet = Tweet(content="Tell me about YieldFi security.", metadata=metadata)
        prompt = generate_interaction_prompt(
            original_tweet=tweet,
            responding_as_account=self.official_account,
            target_account=self.institution_account,
            yieldfi_knowledge_snippet="YieldFi uses multi-layer security protocols."
        )
        # Core checks
        self.assertIn("You are an AI assistant tasked with generating a tweet reply.", prompt)
        self.assertIn(get_base_yieldfi_persona(AccountType.OFFICIAL), prompt)
        self.assertIn(YIELDFI_CORE_MESSAGE, prompt)
        # Original content and author
        self.assertIn('Original Tweet Content: "Tell me about YieldFi security."', prompt)
        self.assertIn(f"Original Tweet Author: @{metadata.author_username}", prompt)
        # Target account persona string
        self.assertIn(f"The original tweet is from @{self.institution_account.username}", prompt)
        # Instruction set
        self.assertIn(get_instruction_set(AccountType.OFFICIAL, AccountType.INSTITUTION), prompt)
        # Knowledge snippet block and content
        self.assertIn("Relevant YieldFi Knowledge Snippet", prompt)
        self.assertIn("YieldFi uses multi-layer security protocols.", prompt)
        # Task description and platform guidance
        self.assertIn("Task: Generate a concise, engaging, and relevant reply to the original tweet", prompt)
        self.assertIn("Ensure the reply is suitable for Twitter", prompt)
        # Ending requirement
        self.assertTrue(prompt.strip().endswith("Do not introduce yourself."))

    def test_generate_interaction_prompt_with_interaction_details(self):
        metadata = TweetMetadata(author_username="UserY")
        tweet = Tweet(content="Cool new feature!", metadata=metadata)
        prompt = generate_interaction_prompt(
            original_tweet=tweet,
            responding_as_account=self.intern_account,
            target_account=self.intern_account,
            interaction_details={'tone_suggestion': 'excited', 'specific_goal': 'share enthusiasm'}
        )
        self.assertIn(get_base_yieldfi_persona(AccountType.INTERN), prompt)
        # Check interaction details inclusion
        self.assertIn("Suggested Tone for reply: excited", prompt)
        self.assertIn("Specific Goal for reply: share enthusiasm", prompt)
        # No knowledge snippet section
        self.assertNotIn("Relevant YieldFi Knowledge Snippet", prompt)

    def test_generate_new_tweet_prompt_with_all_params(self):
        category = TweetCategory(
            name="Product Update",
            description="New feature announcements.",
            prompt_keywords=["launch", "feature"],
            style_guidelines={"tone": "informative", "length": "concise"}
        )
        prompt = generate_new_tweet_prompt(
            category=category,
            active_account=self.official_account,
            topic="Announcing SuperStaker v3!",
            yieldfi_knowledge_snippet="SuperStaker v3 offers auto-compounding."
        )
        self.assertIn("You are an AI assistant tasked with drafting a new Twitter post", prompt)
        self.assertIn(get_base_yieldfi_persona(AccountType.OFFICIAL), prompt)
        self.assertIn(f"Category: {category.name} - {category.description}", prompt)
        self.assertIn("Primary Topic/Key Message: Announcing SuperStaker v3!", prompt)
        self.assertIn("Style Guidelines to follow:", prompt)
        self.assertIn("SuperStaker v3 offers auto-compounding.", prompt)
        self.assertIn("Task: Draft a compelling and informative Twitter post", prompt)
        self.assertIn("Ensure the post is concise, engaging, and suitable for Twitter", prompt)
        self.assertTrue(prompt.strip().endswith("Do not introduce yourself as an AI."))

    def test_generate_new_tweet_prompt_minimal(self):
        category = TweetCategory(
            name="Community Update",
            description="Updates about community events.",
            prompt_keywords=[],
            style_guidelines={}
        )
        prompt = generate_new_tweet_prompt(
            category=category,
            active_account=self.intern_account
        )
        self.assertIn(get_base_yieldfi_persona(AccountType.INTERN), prompt)
        self.assertIn(f"Category: {category.name} - {category.description}", prompt)
        self.assertNotIn("Primary Topic/Key Message:", prompt)
        self.assertTrue(prompt.strip().endswith("Do not introduce yourself as an AI."))

if __name__ == '__main__':
    unittest.main() 