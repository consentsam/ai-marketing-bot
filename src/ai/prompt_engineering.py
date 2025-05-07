# Changelog:
# 2025-05-07 HH:MM - Step 7 - Initial implementation of prompt engineering for dynamic tweet interactions.
# 2025-05-07 HH:MM - Step 18 - Added generate_new_tweet_prompt for category-based tweet creation.

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

from typing import Dict, Any, List, Optional, Tuple
from enum import Enum

try:
    from src.config import get_config
except ImportError:
    from src.config.settings import get_config

from src.models.tweet import Tweet # Or a more generic Post model
from src.models.account import Account, AccountType
from src.models.response import ResponseType # For typing, if creating different prompt structures per response type
from src.models.category import TweetCategory # ADDED FOR STEP 18

# Logger instance - ensure logging is set up if used
# from src.utils.logging import get_logger
# logger = get_logger(__name__) # Use module name for logger

# Core YieldFi message or mission statement that defines the brand voice
YIELDFI_CORE_MESSAGE = get_config("ai.yieldfi_core_message", "YieldFi empowers users with innovative and secure decentralized finance solutions, maximizing yields and providing transparent financial tools.")

class InteractionType(Enum):
    REPLY = "reply"
    NEW_TWEET = "new_tweet"
    ANNOUNCEMENT = "announcement"
    PRODUCT_UPDATE = "product_update"
    COMMUNITY_UPDATE = "community_update"

def get_base_yieldfi_persona(account_type: AccountType) -> str:
    """
    Defines the base persona for YieldFi's social media voice based on the account type.
    
    Args:
        account_type: The type of account posting (e.g., OFFICIAL, INTERN).
    
    Returns:
        A string describing the persona.
    """
    persona_map = {
        AccountType.OFFICIAL: "You are the official voice of YieldFi, a leading decentralized finance platform. Your tone should be professional, authoritative, informative, and trustworthy. Focus on clarity, accuracy, and security. Adhere strictly to YieldFi's brand guidelines and core messaging.",
        AccountType.INTERN: "You are a YieldFi Intern, enthusiastic about DeFi and learning. Your tone should be friendly, helpful, and eager to engage. You can be more informal than the official account but always remain respectful and accurate. Double-check information before sharing.",
        AccountType.PARTNER: "You are representing a YieldFi Partner. Your tone should be collaborative, supportive of YieldFi, and focused on mutual benefits. Highlight the strengths of the partnership.",
        AccountType.KOL: "You are a Key Opinion Leader (KOL) in the DeFi space, associated with YieldFi. Your tone should be influential, insightful, and engaging. Share your expert opinions while aligning with YieldFi's values.",
        AccountType.INSTITUTION: "You are communicating as YieldFi with an institutional entity. Your tone must be highly professional, data-driven, concise, and demonstrate deep understanding of financial markets and regulatory considerations.",
        AccountType.COMMUNITY_MEMBER: "You are a knowledgeable and helpful YieldFi community member. Your tone is supportive, friendly, and aimed at helping other users or discussing YieldFi features positively.",
        AccountType.PARTNER_INTERN: "You are an intern at a YieldFi Partner company. Tone is enthusiastic, learning-focused, and supportive of both your company and YieldFi.",
        AccountType.COMPETITOR: "You are responding to a competitor. Maintain a professional, respectful, and confident tone. Focus on YieldFi's strengths and differentiators without being overtly aggressive.",
        AccountType.UNKNOWN: "You are a general AI assistant providing information about YieldFi. Maintain a neutral, informative, and helpful tone."
    }
    return persona_map.get(account_type, persona_map[AccountType.UNKNOWN])

def get_instruction_set(active_account_type: AccountType, target_account_type: Optional[AccountType]) -> str:
    """
    Selects the appropriate instruction set based on the interacting account types.
    This simulates fetching content from specific instruction documents.
    
    Args:
        active_account_type: The type of account posting.
        target_account_type: The type of account being responded to.
    
    Returns:
        A string with tailored instructions for the interaction.
    """
    if active_account_type == AccountType.OFFICIAL:
        if target_account_type == AccountType.INSTITUTION:
            return "Focus on institutional-grade security, compliance, and robust financial products. Provide data-driven insights."
        elif target_account_type == AccountType.PARTNER:
            return "Emphasize mutual benefits, collaborative opportunities, and shared goals. Reinforce the value of the partnership."
        elif target_account_type == AccountType.COMMUNITY_MEMBER:
            return "Be helpful, informative, and appreciative of community engagement. Address questions clearly."
        else:
            # This else corresponds to the OFFICIAL account type when target is not INSTITUTION, PARTNER, or COMMUNITY
            return "Maintain the official YieldFi voice: professional, authoritative, and informative."
    elif active_account_type == AccountType.INTERN:
        return "Be friendly, helpful, and eager to learn. If unsure, state that you will find out. Double-check information."
    # Add more rules for other personas...
    # Default instruction if no specific rule matches above
    return "Provide a helpful and relevant response."

def generate_interaction_prompt(
    original_tweet: Tweet,
    responding_as_account: Account,
    target_account: Optional[Account] = None,
    yieldfi_knowledge_snippet: Optional[str] = None,
    interaction_details: Optional[Dict[str, Any]] = None,
    platform: str = "Twitter"
) -> str:
    """
    Constructs a detailed prompt for AI interaction based on context.
    
    Args:
        original_tweet: The original tweet being replied to.
        responding_as_account: The account posting the reply.
        target_account: The target account being replied to.
        yieldfi_knowledge_snippet: Relevant YieldFi information to include.
        interaction_details: Dictionary with specific instructions (e.g., tone, goal).
        platform: The social media platform (e.g., Twitter, for character limits).
    
    Returns:
        A formatted string prompt for the AI model.
    """
    # Initialize interaction details if not provided
    if interaction_details is None:
        interaction_details = {}

    persona = get_base_yieldfi_persona(responding_as_account.account_type)
    # Determine original author and target usernames
    original_username = original_tweet.metadata.author_username or ""
    target_username = target_account.username if target_account else original_username
    # Determine display name and account type for target if provided
    target_display = target_account.display_name if target_account else original_username
    target_acc_type = target_account.account_type.value if target_account else ""
    # Single combined string for target persona
    target_persona_str = (
        f"The original tweet is from @{target_username} (Display Name: {target_display}, Account Type: {target_acc_type})"
    )

    instruction_set = get_instruction_set(responding_as_account.account_type, target_account.account_type if target_account else original_tweet.account_type)

    # Ensure original_tweet.content is escaped properly if it contains quotes or special characters
    # A simple way is to replace triple quotes with something else if you want to embed it directly,
    # or just use single/double quotes carefully. For this f-string, we'll ensure it's treated as a block.
    original_content_formatted = original_tweet.content.replace('"''', "'''") # Escape triple quotes if any

    prompt_parts = [
        "You are an AI assistant tasked with generating a tweet reply.",
        f"Your Persona: {persona}",
        "YieldFi Core Message to subtly weave in if relevant: " + YIELDFI_CORE_MESSAGE,
        "--- Original Tweet Context ---",
        f"Original Tweet Author: @{original_username}",
        f'Original Tweet Content: "{original_content_formatted}"',
        target_persona_str,
        "--- End Original Tweet Context ---",
        "--- Instructions for Your Reply ---",
        instruction_set,
    ]

    if interaction_details:
        if "tone_suggestion" in interaction_details:
            prompt_parts.append(f"Suggested Tone for reply: {interaction_details['tone_suggestion']}")
        if "specific_goal" in interaction_details:
            prompt_parts.append(f"Specific Goal for reply: {interaction_details['specific_goal']}")
    
    if yieldfi_knowledge_snippet:
        prompt_parts.append("--- Relevant YieldFi Knowledge Snippet (for context, do not directly quote unless necessary) ---")
        prompt_parts.append(yieldfi_knowledge_snippet)
        prompt_parts.append("--- End Knowledge Snippet ---")

    prompt_parts.append("Task: Generate a concise, engaging, and relevant reply to the original tweet based on all the above information.")
    if platform == "Twitter":
        prompt_parts.append("Ensure the reply is suitable for Twitter (e.g., within character limits, using appropriate hashtags if natural). Do NOT use more than 3 hashtags.")
    
    prompt_parts.append("Your reply should ONLY be the content of the tweet reply itself. Do not add any conversational fluff before or after the tweet content. Do not introduce yourself.")
    return "\n\n".join(prompt_parts)

def generate_new_tweet_prompt(
    category: TweetCategory,
    active_account: Account,
    topic: Optional[str] = None,
    yieldfi_knowledge_snippet: Optional[str] = None,
    platform: str = "Twitter"
) -> str:
    """
    Generates a prompt for creating a new tweet based on a category, topic, and YieldFi knowledge.
    
    Args:
        category: The TweetCategory object defining the tweet's purpose and style.
        active_account: The Account object representing who is posting the tweet.
        topic: Optional user-provided topic or key message for the tweet.
        yieldfi_knowledge_snippet: Optional relevant knowledge about YieldFi.
        platform: The platform for which the tweet is being generated (e.g., "Twitter").
    
    Returns:
        A string prompt for the AI model.
    """
    persona = get_base_yieldfi_persona(active_account.account_type)
    
    prompt_parts = [
        f"You are an AI assistant tasked with drafting a new {platform} post for YieldFi.",
        f"Your Persona: {persona}",
        f"Core YieldFi Message to subtly weave in if relevant: {YIELDFI_CORE_MESSAGE}",
        "--- Tweet Generation Task ---",
        f"Category: {category.name} - {category.description}",
    ]

    if topic:
        prompt_parts.append(f"Primary Topic/Key Message: {topic}")
    
    if category.prompt_keywords:
        prompt_parts.append(f"Helpful Keywords for this category: {', '.join(category.prompt_keywords)}")

    if category.style_guidelines:
        prompt_parts.append("Style Guidelines to follow:")
        for style_key, style_value in category.style_guidelines.items():
            prompt_parts.append(f"  - {style_key.capitalize()}: {style_value}")
    
    if yieldfi_knowledge_snippet:
        prompt_parts.append("--- Relevant YieldFi Knowledge (for context, incorporate naturally) ---")
        prompt_parts.append(yieldfi_knowledge_snippet)
        prompt_parts.append("--- End Knowledge Snippet ---")

    prompt_parts.append(f"Task: Draft a compelling and informative {platform} post based on the category, topic (if provided), and all the above instructions.")
    if platform == "Twitter":
        prompt_parts.append("Ensure the post is concise, engaging, and suitable for Twitter (e.g., within character limits, using appropriate hashtags naturally). Do NOT use more than 3-4 relevant hashtags.")
        prompt_parts.append("If style guidelines specify a length, try to adhere to it. Otherwise, aim for clarity and impact.")

    prompt_parts.append("Your output should ONLY be the content of the tweet itself. Do not add any conversational fluff before or after the tweet content. Do not introduce yourself as an AI.")
    
    return "\n\n".join(prompt_parts)

# The old `create_prompt` and its helpers (`_get_system_context`, `_get_examples`, `_get_response_instructions`)
# would likely be refactored or absorbed into the logic that calls `generate_interaction_prompt`.
# The `