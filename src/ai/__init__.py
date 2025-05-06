"""
AI integration for the YieldFi AI Agent.

This package provides integration with xAI and other AI providers for generating responses.
"""

from src.ai.xai_client import XAIClient
from src.ai.tone_analyzer import analyze_tone
from src.ai.prompt_engineering import create_prompt

__all__ = [
    'XAIClient',
    'analyze_tone',
    'create_prompt'
] 