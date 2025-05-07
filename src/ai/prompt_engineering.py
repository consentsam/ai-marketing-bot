# Changelog:
# 2025-05-06 HH:MM - Step 7 (Anticipation) - Refocus on dynamic generate_reply_prompt, integrate roadmap instructions.

"""
Prompt engineering for the YieldFi AI Agent.

Purpose: Constructs dynamic and contextually relevant prompts for the AI model (e.g., xAI)
         to generate appropriate responses for various social media interactions.
Rationale: Effective prompts are crucial for guiding the LLM to produce outputs that
           align with YieldFi's branding, tone, and specific interaction goals. This module
           encapsulates the logic for creating these prompts based on diverse input factors.
Usage: Called by the `response_generator` module. It takes interaction context
       (like original post, account types, knowledge snippets) and returns a formatted prompt string.
TODOs:
    - Fully implement prompt variations based on all scenarios in Instructions*.md files.
    - Integrate dynamic example loading if hardcoded examples become too numerous.
    - Add prompt generation logic for other platforms (Discord, Telegram) and tasks (news widget).
"""

from typing import Dict, Any, List, Optional

from src.config.settings import get_config # Assuming it's used for some default settings
from src.models.tweet import Tweet # Or a more generic Post model
from src.models.account import Account, AccountType
from src.models.response import ResponseType # For typing, if creating different prompt structures per response type

# Logger instance - ensure logging is set up if used
# from src.utils.logging import get_logger
# logger = get_logger(__name__) # Use module name for logger

# Placeholder for YieldFi specific instructions/knowledge that might be globally relevant to prompts
YIELDFI_CORE_MESSAGE = "YieldFi is the first fully on-chain asset management platform designed for treasuries, funds and defi users, offering Liquid Yield Bearing Tokens (LBTs) across assets. Key products: yUSD, yETH, yBTC. Focus on transparency, security, and high, sustainable yields."

def get_base_yieldfi_persona(active_account_type: AccountType) -> str:
    """Returns the base persona string for YieldFi based on the active account."""
    if active_account_type == AccountType.OFFICIAL:
        return f"You are the official YieldFi (@getyieldFi) social media manager. Your tone is professional, informative, accurate, and aligned with institutional-grade quality. You aim to build trust and showcase YieldFi's strengths."
    elif active_account_type == AccountType.INTERN:
        return f"You are a YieldFi Intern. Your tone is enthusiastic, knowledgeable, helpful, and slightly more casual and engaging than the official account. You can use relevant emojis where appropriate."
    # Add other personas if YieldFi has more distinct voices (e.g., technical support)
    return "You are representing YieldFi, a leading DeFi asset management platform."


def generate_interaction_prompt(
    original_post_content: Optional[str], # Content of the message/tweet being replied to, if any
    active_account_info: Account, # Information about the YieldFi account making the response
    target_account_info: Optional[Account], # Information about the account being interacted with
    yieldfi_knowledge_snippet: str, # Specific, relevant YieldFi data/update
    interaction_details: Dict[str, Any], # Contains goal, specific instructions from files like InstructionsFor*.md
    platform: str = "Twitter" # e.g. "Twitter", "Discord"
) -> str:
    """
    Generates a tailored prompt for various interactions based on extensive context.
    This function aims to be the primary prompt generator for replies and potentially new posts.
    """
    # logger.debug(f"Generating prompt for platform: {platform}, active: {active_account_info.account_type}, target: {target_account_info.account_type if target_account_info else 'N/A'}")

    persona = get_base_yieldfi_persona(active_account_info.account_type)
    prompt_parts = [persona]
    prompt_parts.append(f"Your core mission is to clearly communicate YieldFi's value: {YIELDFI_CORE_MESSAGE}\n")

    if original_post_content:
        prompt_parts.append(f"You are responding to the following {platform} post: \"{original_post_content}\"")
        if target_account_info:
            prompt_parts.append(f"The post is from @{target_account_info.username} (display name: {target_account_info.display_name}, type: {target_account_info.account_type.value}, followers: {target_account_info.follower_count or 'N/A'}).")
            if target_account_info.bio:
                prompt_parts.append(f"Their bio states: \"{target_account_info.bio}\".")
    else:
        prompt_parts.append(f"You are creating a new {platform} post.")

    prompt_parts.append(f"\n## Key YieldFi Information/Context for this response:\n{yieldfi_knowledge_snippet}\n")
    
    # --- Integrating Specific Instructions based on interaction_details ---
    # This is where logic from InstructionsForOfficialToInstitution.md etc. comes in.
    # interaction_details should be populated by the calling function based on these files.
    # Example: interaction_details might contain {'type': 'OfficialToInstitution', 'goal': 'Strategic Praise', 'tone': 'Smart + appreciative', 'example_tweet_if_applicable': '...'}

    specific_instructions = interaction_details.get("instructions_from_doc", "")
    desired_tone = interaction_details.get("tone", "neutral")
    reply_goal = interaction_details.get("goal", "engage effectively")
    example_response_style = interaction_details.get("example_style", "") # Could be an actual example text

    prompt_parts.append(f"## Your Task & Style for this Interaction:")
    if specific_instructions:
        prompt_parts.append(specific_instructions)
    
    prompt_parts.append(f"The goal of your response is to: {reply_goal}.")
    prompt_parts.append(f"Adopt a {desired_tone} tone.")
    if example_response_style:
        prompt_parts.append(f"Consider this style example (do not copy verbatim): '{example_response_style}'")

    # Platform specific constraints
    if platform == "Twitter":
        prompt_parts.append("The response MUST be a single tweet, under 280 characters. Use relevant hashtags sparingly if they add value.")
    elif platform == "Discord":
        prompt_parts.append("The response should be suitable for a Discord channel. You can use Discord markdown formatting if appropriate. Be mindful of channel context if provided.")
    # Add more for Telegram etc.

    prompt_parts.append("\nBased on all the above, generate the response text now:")
    
    final_prompt = "\n\n".join(prompt_parts)
    # logger.debug(f"Generated prompt: {final_prompt}")
    return final_prompt

# The old `create_prompt` and its helpers (`_get_system_context`, `_get_examples`, `_get_response_instructions`)
# would likely be refactored or absorbed into the logic that calls `generate_interaction_prompt`.
# The `generate_reply_prompt` (old one) is also superseded by `generate_interaction_prompt`.
# Keeping them for reference during refactoring for Step 7 is fine, but the goal is one powerful, context-aware prompter.