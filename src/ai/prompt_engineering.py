# Changelog:
# 2025-05-07 HH:MM - Step 7 - Initial refactoring and creation of prompt generation functions.
# 2025-05-07 HH:MM - Step 18 - Updated generate_new_tweet_prompt to use TweetCategory model.
# 2025-05-19 12:00 - Step 25 - Added interaction mode support with mode-specific instructions.
# 2025-05-09 18:20 - Step 408 - Refactored to use parameterized prompt templates from protocol-specific JSON files.

"""
Prompt engineering for the YieldFi AI Agent.

This module provides functions to generate tailored prompts for various AI interactions,
including tweet replies and new tweet generation based on categories.
"""

from enum import Enum
from typing import Dict, Any, Optional, List # Added List
import os
from pathlib import Path

# Attempt to import get_config for robust path finding, fallback if necessary
# This is primarily for modules that might use this utility outside the main app flow
# For instance, if a script directly calls a prompt generator for testing.
try:
    from src.config.settings import get_config, DEFAULT_PROTOCOL
except ImportError:
    # Define a fallback get_config if the main one isn't available
    # This is a simplified version and might not cover all edge cases of the real one
    def get_config(key_path: str, default: Any = None) -> Any:
        # print(f"Warning: Using fallback get_config for key: {key_path}")
        if key_path == "core_message": # Example specific to this module
            return YIELDFI_CORE_MESSAGE
        elif key_path == "protocols.default_protocol":
            return "yieldfi"
        return default
    DEFAULT_PROTOCOL = "yieldfi"  # Fallback default protocol

# Import the prompt template management system
try:
    from src.prompt_management import PromptTemplate, PromptKey
except ImportError:
    logger.warning("Could not import PromptTemplate. Using fallback prompt generation.")
    # This will be handled gracefully in the code below

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

# Step 25: Define available interaction modes
class InteractionMode(Enum):
    DEFAULT = "Default"
    PROFESSIONAL = "Professional"
    DEGEN = "Degen"

# Step 25: Function to load mode-specific instructions
def load_mode_instructions(mode: str = "Default") -> str:
    """
    Loads the instruction file for a specific interaction mode.
    
    Args:
        mode: The interaction mode (Default, Professional, Degen)
        
    Returns:
        A string with the mode-specific instructions, or a fallback if not found
    """
    # Convert mode name to standard format for file lookup
    mode_clean = mode.strip().capitalize().replace(" ", "")
    
    # Use protocol paths from Step 27
    from src.config import get_protocol_path
    mode_file_path = get_protocol_path("mode-instructions", f"InstructionsFor{mode_clean}.md")
    
    if not os.path.exists(mode_file_path):
        logger.warning(f"Mode instruction file not found for '{mode}' at {mode_file_path}. Using fallback.")
        return f"""
        This is a fallback instruction set for '{mode}' mode.
        Use a {mode.lower()} tone and style appropriate for the YieldFi brand.
        """
    
    try:
        with open(mode_file_path, 'r') as file:
            content = file.read()
            logger.info(f"Loaded mode instructions for '{mode}'")
            return content
    except Exception as e:
        logger.error(f"Error loading mode instructions for '{mode}': {e}")
        return f"""
        Error loading mode file for '{mode}'. Using fallback.
        Use a standard, professional tone appropriate for the YieldFi brand.
        """

def get_base_yieldfi_persona(active_account_type: AccountType, mode: str = "Default", protocol_name: str = None) -> str:
    """
    Defines the base persona for YieldFi's social media voice based on the account type and interaction mode.
    
    Args:
        active_account_type: The type of account posting (e.g., OFFICIAL, INTERN).
        mode: The interaction mode (Default, Professional, Degen)
        protocol_name: Optional protocol name to load persona from specific template.
                       If None, uses the default protocol.
    
    Returns:
        A string describing the persona.
    """
    # First try to get the persona from the prompt template system
    try:
        # Convert AccountType enum to string for template lookup
        account_type_str = active_account_type.name if isinstance(active_account_type, AccountType) else str(active_account_type).upper()
        
        # Get persona from template system
        persona = PromptTemplate.get_persona(account_type_str, protocol_name)
        if persona:
            return persona
    except (NameError, AttributeError, Exception) as e:
        # NameError would occur if PromptTemplate isn't imported
        # Fall back to hardcoded personas
        logger.warning(f"Error getting persona from template: {e}. Using fallback.")
        
    # Fallback to hardcoded personas if template system is unavailable or returns empty
    # 1. Default persona for OFFICIAL account:
    if active_account_type == AccountType.OFFICIAL:
        base_persona = """
        You are YieldFi's official account, responsible for maintaining the brand's professional image. 
        Your tone is authoritative yet approachable, knowledgeable about DeFi concepts, and clear in your communication. 
        You represent the company's official positions and announcements.
        """
    
    # 2. Persona for INTERN (more casual, learning-focused):
    elif active_account_type == AccountType.INTERN:
        base_persona = """
        You are YieldFi's intern account. You're enthusiastic about DeFi and crypto, 
        with a more casual and relatable tone. While still knowledgeable, you frame information 
        in simpler, more accessible ways and occasionally show your learning journey.
        """
    
    # 3. Persona for DEVELOPER (technical, behind-the-scenes):
    elif active_account_type == AccountType.DEVELOPER:
        base_persona = """
        You are a YieldFi developer. Your tone is technically focused and straightforward. 
        You speak with authority on the technical aspects of YieldFi's products, 
        occasionally using appropriate technical jargon, while still making the information accessible.
        """
    
    # Default fallback in case an unrecognized account type is provided
    else:
        base_persona = """
        You represent YieldFi on social media. Your goal is to maintain a helpful, 
        knowledgeable tone while providing accurate information about DeFi concepts and YieldFi's offerings.
        """
    
    # Incorporate mode-specific instructions if mode is not Default
    if mode and mode.lower() != "default":
        mode_instructions = load_mode_instructions(mode)
        # Extract key parts from mode instructions for persona modification
        # We mainly want tone guidelines and example style, not the whole file
        sections = mode_instructions.split("##")
        tone_guidelines = ""
        for section in sections:
            if "tone guidelines" in section.lower():
                tone_guidelines = section.strip()
                break
        
        if tone_guidelines:
            base_persona += f"\n\nAdapt your voice according to these mode-specific guidelines:\n{tone_guidelines}"
        else:
            # If we couldn't extract tone guidelines specifically, add a general instruction
            base_persona += f"\n\nAdapt your voice to the {mode} mode, which typically uses a {mode.lower()} tone."
    
    return base_persona

def get_instruction_set(active_account_type: AccountType, target_account_type: AccountType, protocol_name: str = None) -> str:
    """
    Selects the appropriate instruction set based on the interacting account types.
    This simulates fetching content from specific instruction documents.
    
    Args:
        active_account_type: The type of account posting.
        target_account_type: The type of account being responded to.
        protocol_name: Optional protocol name to load instruction set from specific template.
                       If None, uses the default protocol.
    
    Returns:
        A string with tailored instructions for the interaction.
    """
    # First try to get instruction set from the prompt template system
    try:
        # Convert AccountType enums to strings for template lookup
        active_type_str = active_account_type.name if isinstance(active_account_type, AccountType) else str(active_account_type).upper()
        target_type_str = target_account_type.name if isinstance(target_account_type, AccountType) else str(target_account_type).upper()
        
        # Get instruction set from template system
        instruction_set = PromptTemplate.get_instruction_set(active_type_str, target_type_str, protocol_name)
        if instruction_set:
            return instruction_set
    except (NameError, AttributeError, Exception) as e:
        # NameError would occur if PromptTemplate isn't imported
        # Fall back to hardcoded instruction sets
        logger.warning(f"Error getting instruction set from template: {e}. Using fallback.")
    
    # Fallback to hardcoded instruction sets if template system is unavailable or returns empty
    # OFFICIAL account responding to various account types
    if active_account_type == AccountType.OFFICIAL:
        if target_account_type == AccountType.USER:
            return """
            When responding as the official YieldFi account to general users, prioritize clarity and helpfulness.
            Answer questions directly, provide factual information, and maintain a supportive, professional tone.
            """
        elif target_account_type == AccountType.PARTNER:
            return """
            When responding as the official YieldFi account to partners or other projects, emphasize collaboration,
            mutual benefits, and professional courtesy. Acknowledge the partnership value while maintaining
            YieldFi's brand positioning.
            """
        # Add more specific instructions for other target account types as needed
    
    # INTERN account responding to various account types
    elif active_account_type == AccountType.INTERN:
        if target_account_type == AccountType.USER:
            return """
            When responding as the YieldFi intern to general users, be more conversational and personable.
            It's okay to show enthusiasm and use simpler explanations while still being helpful and accurate.
            """
        # Add more specific instructions as needed
    
    # Default instructions if no specific match is found
    return """
    Respond thoughtfully to the context, providing accurate information about YieldFi
    while maintaining appropriate tone and style for your account type.
    """

def generate_interaction_prompt(
    original_post_content: Optional[str],
    active_account_info: Account,
    target_account_info: Optional[Account] = None,
    yieldfi_knowledge_snippet: Optional[str] = None,
    interaction_details: Optional[Dict[str, Any]] = None,
    platform: str = "Twitter",
    mode: str = "Default",  # Added mode parameter
    protocol_name: str = None  # Added protocol_name parameter
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
        mode: The interaction mode (Default, Professional, Degen)
        protocol_name: The name of the protocol to load prompt templates from.
                       If None, uses the default protocol.
    
    Returns:
        A formatted string prompt for the AI model.
    """
    # Initialize interaction details if not provided
    if interaction_details is None:
        interaction_details = {}

    # Try to use the PromptTemplate manager for generating prompt components
    try:
        # Section 1: Persona Definition with mode
        persona = get_base_yieldfi_persona(active_account_info.account_type, mode, protocol_name)
        prompt_parts = [f"Persona: {persona}"]

        # Section 2: Core YieldFi Message
        # Try to get core message from template, fall back to the constant if not available
        core_message = PromptTemplate.get(PromptKey.CORE_MESSAGE, protocol_name) or YIELDFI_CORE_MESSAGE
        prompt_parts.append(f"Core Message: {core_message.strip()}")

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
            instructions = get_instruction_set(
                active_account_info.account_type, 
                target_account_info.account_type, 
                protocol_name
            )
            prompt_parts.append(f"Interaction Instructions: {instructions.strip()}")

        # Section 5: Relevant YieldFi Knowledge (if available)
        if yieldfi_knowledge_snippet:
            prompt_parts.append(f"Relevant YieldFi Knowledge: {yieldfi_knowledge_snippet}")

        # Section 6: Task-Specific Instructions (from interaction_details or default)
        tone = interaction_details.get('tone', 'default')
        goal = interaction_details.get('goal', 'engage and inform')
        style_examples = interaction_details.get('style_examples', '')
        task_instructions = f"Task: Craft a response that aligns with the persona and core message."
        
        # If mode is not Default, get mode details from template
        if mode.lower() != "default":
            # Try to get mode details from template
            mode_details = PromptTemplate.get_interaction_mode(mode, protocol_name)
            if mode_details:
                # If mode has tone and style information, use it
                if 'tone' in mode_details:
                    prompt_parts.append(f"Mode-Specific Tone: {mode_details['tone']}")
                if 'style' in mode_details:
                    prompt_parts.append(f"Mode-Specific Style: {mode_details['style']}")
                if 'examples' in mode_details and isinstance(mode_details['examples'], list):
                    examples_text = "\n".join([f"- {ex}" for ex in mode_details['examples']])
                    prompt_parts.append(f"Mode-Specific Examples:\n{examples_text}")
            else:
                # Fall back to loading mode instructions from file
                mode_instructions = load_mode_instructions(mode)
                sections = mode_instructions.split("##")
                examples_section = ""
                for section in sections:
                    if "examples" in section.lower():
                        examples_section = section.strip()
                
                if examples_section:
                    prompt_parts.append(f"Mode-Specific Style Examples: {examples_section}")
        
        if tone != 'default':
            task_instructions += f" Use a {tone} tone."
        task_instructions += f" Goal: {goal}."
        if style_examples:
            task_instructions += f" Style Examples: {style_examples}"
        
        # Platform-specific constraints
        if platform.lower() == "twitter":
            task_instructions += " Keep the response under 280 characters as per Twitter's limit."
        prompt_parts.append(task_instructions)

        # Assemble the final prompt, prepending critical instructions to ensure they are not truncated
        # Get critical instructions from template or use default
        critical_instr = PromptTemplate.get_critical_instructions(platform.lower(), protocol_name)
        if critical_instr:
            instruction_block = "CRITICAL INSTRUCTIONS:\n" + "\n".join([f"{i+1}. {instr}" for i, instr in enumerate(critical_instr)])
        else:
            # Fallback critical instructions
            instruction_block = """
CRITICAL INSTRUCTIONS:
1. Respond with ONLY the final tweet text
2. Maximum 280 characters for Twitter
3. NO explanations, reasoning, self-talk, or any other content
4. NO prefixes like 'Tweet:' or 'Response:'
5. Do NOT include character counts or drafts
6. Your ENTIRE response should be JUST the tweet
"""
        
        final_prompt_body = "\n\n".join(prompt_parts)
        
        # Get response prefix from template or use default
        response_prefix = PromptTemplate.get(PromptKey.RESPONSE_PREFIX, protocol_name) or "Response:"
        
        final_prompt = instruction_block + "\n\n" + final_prompt_body + "\n\n" + response_prefix
        logger.debug(f"Generated INTERACTION prompt: {final_prompt}")
        return final_prompt
        
    except (NameError, AttributeError, Exception) as e:
        # Fall back to the original implementation if PromptTemplate is not available or fails
        logger.warning(f"Error using PromptTemplate for prompt generation: {e}. Using fallback logic.")
        
        # Original implementation (fallback)
        # Section 1: Persona Definition with mode
        persona = get_base_yieldfi_persona(active_account_info.account_type, mode)
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
        
        # If mode is not Default, incorporate mode-specific style guidelines
        if mode.lower() != "default":
            # Load full mode instructions to extract style examples specific to this mode
            mode_instructions = load_mode_instructions(mode)
            sections = mode_instructions.split("##")
            examples_section = ""
            for section in sections:
                if "examples" in section.lower():
                    examples_section = section.strip()
            
            if examples_section:
                prompt_parts.append(f"Mode-Specific Style Examples: {examples_section}")
        
        if tone != 'default':
            task_instructions += f" Use a {tone} tone."
        task_instructions += f" Goal: {goal}."
        if style_examples:
            task_instructions += f" Style Examples: {style_examples}"
        # Platform-specific constraints
        if platform.lower() == "twitter":
            task_instructions += " Keep the response under 280 characters as per Twitter's limit."
        prompt_parts.append(task_instructions)

        # Assemble the final prompt, prepending critical instructions to ensure they are not truncated
        instruction_block = """
CRITICAL INSTRUCTIONS:
1. Respond with ONLY the final tweet text
2. Maximum 280 characters for Twitter
3. NO explanations, reasoning, self-talk, or any other content
4. NO prefixes like 'Tweet:' or 'Response:'
5. Do NOT include character counts or drafts
6. Your ENTIRE response should be JUST the tweet
"""
        final_prompt_body = "\n\n".join(prompt_parts)
        final_prompt = instruction_block + "\n\n" + final_prompt_body + "\n\nResponse:"
        logger.debug(f"Generated INTERACTION prompt: {final_prompt}")
        return final_prompt

def generate_new_tweet_prompt(
    category: TweetCategory, # Changed from str to TweetCategory
    topic: Optional[str] = None,
    yieldfi_knowledge_snippet: Optional[str] = None,
    active_account_info: Account = None, # Should ideally not be None
    platform: str = "Twitter",
    additional_instructions: Optional[Dict[str, Any]] = None, # Added for more flexibility
    mode: str = "Default",  # Added mode parameter
    protocol_name: str = None  # Added protocol_name parameter
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
        mode: The interaction mode (Default, Professional, Degen)
        protocol_name: The name of the protocol to load prompt templates from.
                       If None, uses the default protocol.

    Returns:
        A formatted string prompt for the AI model.
    """
    # Initialize if not provided
    if additional_instructions is None:
        additional_instructions = {}
    
    # Try to use the PromptTemplate manager for generating prompt components
    try:
        # Create prompt parts in sequence
        prompt_parts = []

        # Section 1: Persona Definition with mode
        if active_account_info is not None:
            persona = get_base_yieldfi_persona(active_account_info.account_type, mode, protocol_name)
            prompt_parts.append(f"Persona: {persona}")
        else:
            # Use a generic official persona if no active account info provided
            persona = get_base_yieldfi_persona(AccountType.OFFICIAL, mode, protocol_name) # Fallback to OFFICIAL
            prompt_parts.append(f"Persona: {persona}")

        # Section 2: Core YieldFi Message
        # Try to get core message from template, fall back to the constant if not available
        core_message = PromptTemplate.get(PromptKey.CORE_MESSAGE, protocol_name) or YIELDFI_CORE_MESSAGE
        prompt_parts.append(f"Core Message: {core_message.strip()}")

        # Section 3: Tweet Category
        # Handle TweetCategory object for Step 18
        prompt_parts.append(f"Tweet Category: {category.name}")
        prompt_parts.append(f"Category Description: {category.description}")
        
        # Include category-specific style guidelines if present (Step 18)
        if hasattr(category, 'style_guidelines') and category.style_guidelines:
            style_points = []
            for style_key, style_value in category.style_guidelines.items():
                # Format each style guideline as a readable point
                if style_key == 'hashtags' and isinstance(style_value, list):
                    hashtags_formatted = ', '.join([f'#{tag}' for tag in style_value])
                    style_points.append(f"Suggested Hashtags: {hashtags_formatted}")
                elif style_key != 'length': # Length is handled separately in task instructions
                    style_points.append(f"{style_key.replace('_', ' ').title()}: {style_value}")
            
            if style_points:
                prompt_parts.append("Style Guidelines:\n- " + "\n- ".join(style_points))

        # Section 4: Topic Information (if provided)
        if topic:
            prompt_parts.append(f"Topic: {topic}")
        
        # Section 4.5: Mode-specific Style (if not Default)
        if mode.lower() != "default":
            # Try to get mode details from template
            mode_details = PromptTemplate.get_interaction_mode(mode, protocol_name)
            if mode_details:
                # If mode has tone and style information, use it
                if 'tone' in mode_details:
                    prompt_parts.append(f"Mode-Specific Tone: {mode_details['tone']}")
                if 'style' in mode_details:
                    prompt_parts.append(f"Mode-Specific Style: {mode_details['style']}")
                if 'examples' in mode_details and isinstance(mode_details['examples'], list):
                    examples_text = "\n".join([f"- {ex}" for ex in mode_details['examples']])
                    prompt_parts.append(f"Mode-Specific Examples:\n{examples_text}")
            else:
                # Fall back to loading mode instructions from file
                mode_instructions = load_mode_instructions(mode)
                sections = mode_instructions.split("##")
                examples_section = ""
                style_points = ""
                
                for section in sections:
                    if "examples" in section.lower():
                        examples_section = section.strip()
                    elif "style points" in section.lower():
                        style_points = section.strip()
                
                if examples_section or style_points:
                    mode_style = f"Mode-Specific Style ({mode}):"
                    if examples_section:
                        mode_style += f"\n{examples_section}"
                    if style_points:
                        mode_style += f"\n{style_points}"
                    prompt_parts.append(mode_style)

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
        
        # Add mode-specific instruction
        if mode.lower() != "default":
            task_instructions_list.append(f"Use the {mode} interaction style as detailed above.")

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

        prompt_parts.append("\n".join(task_instructions_list))

        # Assemble the final prompt, prepending critical instructions to avoid truncation
        # Get critical instructions from template or use default
        critical_instr = PromptTemplate.get_critical_instructions(platform.lower(), protocol_name)
        if critical_instr:
            instruction_block = "CRITICAL INSTRUCTIONS:\n" + "\n".join([f"{i+1}. {instr}" for i, instr in enumerate(critical_instr)])
        else:
            # Fallback critical instructions
            instruction_block = """
CRITICAL INSTRUCTIONS:
1. Respond with ONLY the final tweet text
2. Maximum 280 characters for Twitter
3. NO explanations, reasoning, self-talk, or any other content
4. NO prefixes like 'Tweet:' or 'Response:'
5. Do NOT include character counts or drafts
6. Your ENTIRE response should be JUST the tweet
"""
        
        final_prompt_body = "\n\n".join(prompt_parts)
        
        # Get response prefix from template or use default
        response_prefix = PromptTemplate.get(PromptKey.RESPONSE_PREFIX, protocol_name) or "Tweet:"
        
        final_prompt = instruction_block + "\n\n" + final_prompt_body + "\n\n" + response_prefix
        logger.debug(f"Generated NEW TWEET prompt: {final_prompt}")
        return final_prompt
        
    except (NameError, AttributeError, Exception) as e:
        # Fall back to the original implementation if PromptTemplate is not available or fails
        logger.warning(f"Error using PromptTemplate for prompt generation: {e}. Using fallback logic.")
        
        # Original implementation (fallback)
        # Create prompt parts in sequence
        prompt_parts = []

        # Section 1: Persona Definition with mode
        if active_account_info is not None:
            persona = get_base_yieldfi_persona(active_account_info.account_type, mode)
            prompt_parts.append(f"Persona: {persona}")
        else:
            # Use a generic official persona if no active account info provided
            persona = get_base_yieldfi_persona(AccountType.OFFICIAL, mode) # Fallback to OFFICIAL
            prompt_parts.append(f"Persona: {persona}")

        # Section 2: Core YieldFi Message
        prompt_parts.append(f"Core Message: {YIELDFI_CORE_MESSAGE.strip()}")

        # Section 3: Tweet Category
        # Handle TweetCategory object for Step 18
        prompt_parts.append(f"Tweet Category: {category.name}")
        prompt_parts.append(f"Category Description: {category.description}")
        
        # Include category-specific style guidelines if present (Step 18)
        if hasattr(category, 'style_guidelines') and category.style_guidelines:
            style_points = []
            for style_key, style_value in category.style_guidelines.items():
                # Format each style guideline as a readable point
                if style_key == 'hashtags' and isinstance(style_value, list):
                    hashtags_formatted = ', '.join([f'#{tag}' for tag in style_value])
                    style_points.append(f"Suggested Hashtags: {hashtags_formatted}")
                elif style_key != 'length': # Length is handled separately in task instructions
                    style_points.append(f"{style_key.replace('_', ' ').title()}: {style_value}")
            
            if style_points:
                prompt_parts.append("Style Guidelines:\n- " + "\n- ".join(style_points))

        # Section 4: Topic Information (if provided)
        if topic:
            prompt_parts.append(f"Topic: {topic}")
        
        # Section 4.5: Mode-specific Style (if not Default)
        if mode.lower() != "default":
            # Load mode instructions to extract style examples specific to this mode
            mode_instructions = load_mode_instructions(mode)
            sections = mode_instructions.split("##")
            examples_section = ""
            style_points = ""
            
            for section in sections:
                if "examples" in section.lower():
                    examples_section = section.strip()
                elif "style points" in section.lower():
                    style_points = section.strip()
            
            if examples_section or style_points:
                mode_style = f"Mode-Specific Style ({mode}):"
                if examples_section:
                    mode_style += f"\n{examples_section}"
                if style_points:
                    mode_style += f"\n{style_points}"
                prompt_parts.append(mode_style)

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
        
        # Add mode-specific instruction
        if mode.lower() != "default":
            task_instructions_list.append(f"Use the {mode} interaction style as detailed above.")

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

        prompt_parts.append("\n".join(task_instructions_list))

        # Assemble the final prompt, prepending critical instructions to avoid truncation
        instruction_block_new = """
CRITICAL INSTRUCTIONS:
1. Respond with ONLY the final tweet text
2. Maximum 280 characters for Twitter
3. NO explanations, reasoning, self-talk, or any other content
4. NO prefixes like 'Tweet:' or 'Response:'
5. Do NOT include character counts or drafts
6. Your ENTIRE response should be JUST the tweet
"""
        final_prompt_body_new = "\n\n".join(prompt_parts)
        final_prompt = instruction_block_new + "\n\n" + final_prompt_body_new + "\n\nTweet:"
        logger.debug(f"Generated NEW TWEET prompt: {final_prompt}")
        return final_prompt

# The old `create_prompt` and its helpers (`_get_system_context`, `_get_examples`, `_get_response_instructions`)
# would likely be refactored or absorbed into the logic that calls `generate_interaction_prompt`.
# The `generate_reply_prompt` (old one) is also superseded by `generate_interaction_prompt`.
# Keeping them for reference during refactoring for Step 7 is fine, but the goal is one powerful, context-aware prompter.