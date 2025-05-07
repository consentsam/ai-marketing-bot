# Changelog:
# 2025-05-07 HH:MM - Step 7 - Initial implementation of prompt engineering for dynamic tweet interactions.

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

# Logger instance - ensure logging is set up if used
# from src.utils.logging import get_logger
# logger = get_logger(__name__) # Use module name for logger

# Core YieldFi message or mission statement that defines the brand voice
YIELDFI_CORE_MESSAGE = """
YieldFi is a leading DeFi platform focused on providing innovative yield farming solutions, secure staking, and transparent financial tools. Our mission is to empower users with accessible, decentralized financial opportunities while maintaining the highest standards of security and trust.
"""

class InteractionType(Enum):
    REPLY = "reply"
    NEW_TWEET = "new_tweet"
    ANNOUNCEMENT = "announcement"
    PRODUCT_UPDATE = "product_update"
    COMMUNITY_UPDATE = "community_update"

def get_base_yieldfi_persona(active_account_type: AccountType) -> str:
    """
    Defines the base persona for YieldFi's social media voice based on the account type.
    
    Args:
        active_account_type: The type of account posting (e.g., OFFICIAL, INTERN).
    
    Returns:
        A string describing the persona.
    """
    if active_account_type == AccountType.OFFICIAL:
        return "You are the official voice of YieldFi, a professional, authoritative, and helpful representative of the company. Your tone is polished, confident, and focused on building trust and providing value."
    elif active_account_type == AccountType.INTERN:
        return "You are a YieldFi intern, enthusiastic, approachable, and relatable. Your tone is casual, friendly, and eager to learn or help, often adding a personal touch or humor when appropriate."
    elif active_account_type == AccountType.PARTNER:
        return "You are a YieldFi partner, collaborative and supportive. Your tone is professional yet warm, emphasizing mutual benefits and shared goals."
    else:
        return "You are a representative of YieldFi, maintaining a balanced and engaging tone that aligns with the brand's mission to empower users through decentralized finance."

def get_instruction_set(active_account_type: AccountType, target_account_type: AccountType) -> str:
    """
    Selects the appropriate instruction set based on the interacting account types.
    This simulates fetching content from specific instruction documents.
    
    Args:
        active_account_type: The type of account posting.
        target_account_type: The type of account being responded to.
    
    Returns:
        A string with tailored instructions for the interaction.
    """
    if active_account_type == AccountType.OFFICIAL and target_account_type == AccountType.INSTITUTION:
        return """
        When responding to institutions, maintain a highly professional tone. Focus on potential collaborations, emphasizing YieldFi's robust security, high yields, and transparency. Highlight case studies or data if relevant. Avoid casual language and ensure responses are concise and value-driven.
        Example tone: 'We're impressed by your institution's track record and believe a partnership with YieldFi could enhance your portfolio with our secure, high-yield DeFi solutions. Let's discuss further.'
        """
    elif active_account_type == AccountType.OFFICIAL and target_account_type == AccountType.PARTNER:
        return """
        When engaging with partners, adopt a collaborative and appreciative tone. Acknowledge shared goals or past successes, and suggest ways YieldFi can support their initiatives through our platform. Keep the tone warm but professional.
        Example tone: 'Thank you for being a valued partner. We're excited to explore how YieldFi's latest staking options can benefit your community. Can we schedule a call to discuss?' 
        """
    elif active_account_type == AccountType.INTERN and target_account_type == AccountType.INTERN:
        return """
        When interacting with other interns, be friendly, supportive, and relatable. Share personal insights or excitement about YieldFi's features, ask questions, or offer help in a casual way. Use emojis sparingly if the context allows.
        Example tone: 'Hey, I've been diving into YieldFi's yield farming pools lately, and they're amazing! Have you tried them yet? Let me know if you want some tips 😊'
        """
    else:
        return """
        Tailor your response to the context of the interaction. Maintain YieldFi's brand voice, focusing on empowerment, innovation, and trust in decentralized finance. Be helpful, clear, and engaging, adjusting formality based on the target audience.
        """

def generate_interaction_prompt(
    original_post_content: Optional[str],
    active_account_info: Account,
    target_account_info: Optional[Account] = None,
    yieldfi_knowledge_snippet: Optional[str] = None,
    interaction_details: Optional[Dict[str, Any]] = None,
    platform: str = "Twitter"
) -> str:
    """
    Constructs a detailed prompt for AI interaction based on context.
    
    Args:
        original_post_content: Content of the post/tweet being replied to, if any.
        active_account_info: Information about the account posting (YieldFi persona).
        target_account_info: Information about the target account (if replying).
        yieldfi_knowledge_snippet: Relevant YieldFi information to include.
        interaction_details: Dictionary with specific instructions (e.g., tone, goal).
        platform: The social media platform (e.g., Twitter, for character limits).
    
    Returns:
        A formatted string prompt for the AI model.
    """
    # Initialize interaction details if not provided
    if interaction_details is None:
        interaction_details = {}

    # Section 1: Persona Definition
    persona = get_base_yieldfi_persona(active_account_info.account_type)
    prompt_parts = [f"Persona: {persona}"]

    # Section 2: Core YieldFi Message
    prompt_parts.append(f"Core Message: {YIELDFI_CORE_MESSAGE.strip()}")

    # Section 3: Original Post Context (if replying)
    if original_post_content:
        prompt_parts.append(f"Original Post to Reply To: \"{original_post_content}\"")

    # Section 4: Target Account Context (if available)
    if target_account_info:
        target_desc = f"Target Account: @{target_account_info.username} (Type: {target_account_info.account_type.value})"
        if target_account_info.bio:
            target_desc += f", Bio: {target_account_info.bio}"
        prompt_parts.append(target_desc)
        # Add specific instructions based on account types
        instructions = get_instruction_set(active_account_info.account_type, target_account_info.account_type)
        prompt_parts.append(f"Interaction Instructions: {instructions.strip()}")

    # Section 5: Relevant YieldFi Knowledge (if available)
    if yieldfi_knowledge_snippet:
        prompt_parts.append(f"Relevant YieldFi Knowledge: {yieldfi_knowledge_snippet}")

    # Section 6: Task-Specific Instructions (from interaction_details or default)
    tone = interaction_details.get('tone', 'default')
    goal = interaction_details.get('goal', 'engage and inform')
    style_examples = interaction_details.get('style_examples', '')
    task_instructions = f"Task: Craft a response that aligns with the persona and core message."
    if tone != 'default':
        task_instructions += f" Use a {tone} tone."
    task_instructions += f" Goal: {goal}."
    if style_examples:
        task_instructions += f" Style Examples: {style_examples}"
    # Platform-specific constraints
    if platform.lower() == "twitter":
        task_instructions += " Keep the response under 280 characters as per Twitter's limit."
    prompt_parts.append(task_instructions)

    # Combine all parts into the final prompt
    final_prompt = "\n\n".join(prompt_parts)
    final_prompt += "\n\nResponse: "
    return final_prompt

def generate_new_tweet_prompt(
    category: str,
    topic: Optional[str] = None,
    yieldfi_knowledge_snippet: Optional[str] = None,
    active_account_info: Account = None,
    platform: str = "Twitter"
) -> str:
    """
    Constructs a prompt for creating a new tweet based on a category and topic.
    
    Args:
        category: The category of the tweet (e.g., Announcement, Community Update).
        topic: Specific topic or content focus for the tweet.
        yieldfi_knowledge_snippet: Relevant YieldFi information to include.
        active_account_info: Information about the account posting.
        platform: The social media platform (e.g., Twitter).
    
    Returns:
        A formatted string prompt for the AI model.
    """
    # Section 1: Persona Definition
    if active_account_info:
        persona = get_base_yieldfi_persona(active_account_info.account_type)
    else:
        persona = get_base_yieldfi_persona(AccountType.OFFICIAL)
    prompt_parts = [f"Persona: {persona}"]

    # Section 2: Core YieldFi Message
    prompt_parts.append(f"Core Message: {YIELDFI_CORE_MESSAGE.strip()}")

    # Section 3: Category and Topic
    category_desc = f"Tweet Category: {category}"
    if topic:
        category_desc += f"\nSpecific Topic: {topic}"
    prompt_parts.append(category_desc)

    # Section 4: Relevant YieldFi Knowledge (if available)
    if yieldfi_knowledge_snippet:
        prompt_parts.append(f"Relevant YieldFi Knowledge: {yieldfi_knowledge_snippet}")

    # Section 5: Task Instructions
    task_instructions = f"Task: Create a new tweet that aligns with the persona and core message for the specified category."
    if platform.lower() == "twitter":
        task_instructions += " Keep the tweet under 280 characters as per Twitter's limit."
    prompt_parts.append(task_instructions)

    # Combine all parts into the final prompt
    final_prompt = "\n\n".join(prompt_parts)
    final_prompt += "\n\nTweet: "
    return final_prompt

# The old `create_prompt` and its helpers (`_get_system_context`, `_get_examples`, `_get_response_instructions`)
# would likely be refactored or absorbed into the logic that calls `generate_interaction_prompt`.
# The `generate_reply_prompt` (old one) is also superseded by `generate_interaction_prompt`.
# Keeping them for reference during refactoring for Step 7 is fine, but the goal is one powerful, context-aware prompter.