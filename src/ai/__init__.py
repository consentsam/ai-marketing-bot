# src/ai/__init__.py - Created 2025-05-07

# Changelog:
# 2025-05-07 HH:MM - Step 7 - Initial exports for prompt engineering.
# 2025-05-07 HH:MM - Step 8 - Exported tone analysis functions.
# 2025-05-07 HH:MM - Step 9 - Exported response generation functions.
# 2025-05-07 HH:MM - Step 18 - Exported generate_new_tweet_prompt.

"""
AI package for the YieldFi AI Agent.

This package includes modules for AI client interaction, prompt engineering,
response generation, and tone analysis.
"""

from .xai_client import XAIClient
from .prompt_engineering import (
    generate_interaction_prompt,
    generate_new_tweet_prompt,
    get_base_yieldfi_persona,
    get_instruction_set
)
from .tone_analyzer import analyze_tone, analyze_tweet_tone
from .response_generator import generate_tweet_reply, generate_new_tweet
# Placeholder for other AI components to be added in later steps
# from .response_generator import generate_tweet_reply

__all__ = [
    "XAIClient",
    "generate_interaction_prompt",
    "generate_new_tweet_prompt",
    "get_base_yieldfi_persona",
    "get_instruction_set",
    "analyze_tone",
    "analyze_tweet_tone",
    "generate_tweet_reply",
    "generate_new_tweet",
    # 'generate_tweet_reply',
]