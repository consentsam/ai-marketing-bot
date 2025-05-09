# Changelog:
# 2025-05-07 HH:MM - Step 7 - Initial refactoring and creation of prompt generation functions.
# 2025-05-07 HH:MM - Step 18 - Updated generate_new_tweet_prompt to use TweetCategory model.

"""
Prompt engineering for the YieldFi AI Agent.

This module provides functions to generate tailored prompts for various AI interactions,
including tweet replies and new tweet generation based on categories.
"""

from enum import Enum
from typing import Dict, Any, Optional, List # Added List

# Attempt to import get_config for robust path finding, fallback if necessary
# This is primarily for modules that might use this utility outside the main app flow
# For instance, if a script directly calls a prompt generator for testing.
try:
    from src.config.settings import get_config
except ImportError:
    # Define a fallback get_config if the main one isn't available
    # This is a simplified version and might not cover all edge cases of the real one
    def get_config(key_path: str, default: Any = None) -> Any:
        # print(f"Warning: Using fallback get_config for key: {key_path}")
        if key_path == "core_message": # Example specific to this module
            return YIELDFI_CORE_MESSAGE
        return default

from src.models.tweet import Tweet # Or a more generic Post model
from src.models.account import Account, AccountType
from src.models.response import ResponseType # For typing, if creating different prompt structures per response type
from src.models.category import TweetCategory # Added for Step 18

# Logger instance - ensure logging is set up if used
from src.utils.logging import get_logger # type: ignore
logger = get_logger(__name__) # Use module name for logger

# Core YieldFi message or mission statement that defines the brand voice
YIELDFI_CORE_MESSAGE = get_config("yieldfi.core_message", """
YieldFi is a leading DeFi platform focused on providing innovative yield farming solutions, secure staking, and transparent financial tools. Our mission is to empower users with accessible, decentralized financial opportunities while maintaining the highest standards of security and trust.
""")

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
    final_prompt += """\n\n
CRITICAL INSTRUCTIONS:
1. Respond with ONLY the final tweet text
2. Maximum 280 characters for Twitter
3. NO explanations, reasoning, or self-talk before or after
4. NO prefixes like 'Tweet:' or 'Response:'
5. Do NOT include character counts or drafts

Response:"""
    logger.debug(f"Generated INTERACTION prompt: {final_prompt}")
    return final_prompt

def generate_new_tweet_prompt(
    category: TweetCategory, # Changed from str to TweetCategory
    topic: Optional[str] = None,
    yieldfi_knowledge_snippet: Optional[str] = None,
    active_account_info: Account = None, # Should ideally not be None
    platform: str = "Twitter",
    additional_instructions: Optional[Dict[str, Any]] = None # Added for more flexibility
) -> str:
    """
    Constructs a prompt for creating a new tweet based on a category and topic.
    
    Args:
        category: The TweetCategory object for the tweet.
        topic: Specific topic or content focus for the tweet.
        yieldfi_knowledge_snippet: Relevant YieldFi information to include.
        active_account_info: Information about the account posting.
        platform: The social media platform (e.g., Twitter).
        additional_instructions: Optional dictionary for any other specific instructions.

    Returns:
        A formatted string prompt for the AI model.
    """
    if additional_instructions is None:
        additional_instructions = {}

    # Allow category to be provided as a string
    if isinstance(category, str):
        category = TweetCategory(name=category, description="", prompt_keywords=[], style_guidelines={})

    # Section 1: Persona Definition
    if active_account_info:
        persona = get_base_yieldfi_persona(active_account_info.account_type)
    else:
        # Fallback to official persona if active_account_info is not provided
        # Though in practice, it should always be provided from the UI/controller.
        persona = get_base_yieldfi_persona(AccountType.OFFICIAL)
    prompt_parts = [f"Persona: {persona}"]

    # Section 2: Core YieldFi Message
    prompt_parts.append(f"Core Message: {YIELDFI_CORE_MESSAGE.strip()}")

    # Section 3: Category and Topic
    prompt_parts.append(f"Tweet Category: {category.name}")
    prompt_parts.append(f"Category Description: {category.description}")
    if category.prompt_keywords:
        prompt_parts.append(f"Category Keywords: {', '.join(category.prompt_keywords)}")
    
    if topic:
        prompt_parts.append(f"Specific Topic: {topic}")

    # Section 4: Style Guidelines from Category
    if category.style_guidelines:
        style_parts = ["Style Guidelines:"]
        for key, value in category.style_guidelines.items():
            style_parts.append(f"  - {key.replace('_', ' ').capitalize()}: {value}")
        prompt_parts.append("\n".join(style_parts))

    # Section 5: Relevant YieldFi Knowledge (if available)
    if yieldfi_knowledge_snippet:
        prompt_parts.append(f"Relevant YieldFi Knowledge: {yieldfi_knowledge_snippet}")

    # Section 6: Task Instructions
    # Define initial task instruction, using 'tweet' wording for Twitter
    if platform.lower() == "twitter":
        initial_instruction = "Task: Create a new tweet that aligns with the persona, core message, and the specified category details."
    else:
        initial_instruction = f"Task: Create a new {platform} post that aligns with the persona, core message, and the specified category details."
    task_instructions_list = [
        initial_instruction
    ]

    # Incorporate additional_instructions
    custom_tone = additional_instructions.get('tone')
    custom_goal = additional_instructions.get('goal')
    if custom_tone:
        task_instructions_list.append(f"Ensure the tone is specifically: {custom_tone}.")
    if custom_goal:
        task_instructions_list.append(f"The primary goal is: {custom_goal}.")

    if platform.lower() == "twitter":
        # Check if category style_guidelines already has length constraint
        length_constraint = category.style_guidelines.get('length', "Keep the tweet under 280 characters as per Twitter's limit.")
        if "characters" not in length_constraint.lower(): # Avoid duplicate length constraints
            length_constraint = "Keep the tweet under 280 characters as per Twitter's limit. " + length_constraint
        task_instructions_list.append(length_constraint)
    
    # Include any other specific instructions from the category or additional_instructions
    # For example, if category.style_guidelines has 'hashtags' or 'call_to_action'
    # These are now part of the Style Guidelines section, but could be reiterated here if needed.

    prompt_parts.append("\n".join(task_instructions_list))

    # Combine all parts into the final prompt
    final_prompt = "\n\n".join(prompt_parts)
    final_prompt += """\n\n
CRITICAL INSTRUCTIONS:
1. Respond with ONLY the final tweet text
2. Maximum 280 characters for Twitter
3. NO explanations, reasoning, or self-talk before or after
4. NO prefixes like 'Tweet:' or 'Response:'
5. Do NOT include character counts or drafts

Tweet:"""
    logger.debug(f"Generated NEW TWEET prompt: {final_prompt}")
    return final_prompt

# The old `create_prompt` and its helpers (`_get_system_context`, `_get_examples`, `_get_response_instructions`)
# would likely be refactored or absorbed into the logic that calls `generate_interaction_prompt`.
# The `generate_reply_prompt` (old one) is also superseded by `generate_interaction_prompt`.
# Keeping them for reference during refactoring for Step 7 is fine, but the goal is one powerful, context-aware prompter.