# src/ai/__init__.py - Created 2025-05-07

# Changelog:
# 2025-05-07 HH:MM - Step 7 - Exported prompt engineering functions.
# 2025-05-07 HH:MM - Step 8 - Exported tone analysis functions.
# 2025-05-07 HH:MM - Step 9 - Exported response generator functions.
# 2025-05-19 12:00 - Step 25 - Added InteractionMode and mode-related functions.

"""
AI module for the YieldFi AI Agent.

This package contains modules related to AI functionalities,
including API clients, prompt engineering, tone analysis, and response generation.
"""

from .xai_client import XAIClient
from .prompt_engineering import (
    generate_interaction_prompt, 
    generate_new_tweet_prompt,
    get_base_yieldfi_persona, # Added during step 7 testing, ensure it's exported
    get_instruction_set, # Added during step 7 testing, ensure it's exported
    InteractionMode,  # Added in Step 25
    load_mode_instructions  # Added in Step 25
)
from .tone_analyzer import analyze_tone, analyze_tweet_tone
from .response_generator import generate_tweet_reply, generate_new_tweet
from .relevancy import get_facts  # Added in Step 26 relevancy facts
# Placeholder for other AI components to be added in later steps
# from .response_generator import generate_tweet_reply

__all__ = [
    'XAIClient',
    'generate_interaction_prompt',
    'generate_new_tweet_prompt',
    'get_base_yieldfi_persona',
    'get_instruction_set',
    'analyze_tone',
    'analyze_tweet_tone',
    'generate_tweet_reply',
    'generate_new_tweet',
    'InteractionMode',  # Added in Step 25
    'load_mode_instructions',  # Added in Step 25
    'get_facts'  # Added in Step 26
    # 'generate_tweet_reply',
]