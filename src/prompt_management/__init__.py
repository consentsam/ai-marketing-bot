# Changelog:
# 2025-05-09 18:15 - Step 408 - Created prompt_management module for parameterized prompt templates.

"""
prompt_management package for handling prompt templates across different protocols.
This module provides functionality to load, cache, and access prompt templates from JSON files.
"""

from .template_loader import PromptTemplate, PromptKey
