# Changelog:
# 2025-05-07 HH:MM - Step 5 - Export get_config and load_config functions.
# 2025-05-07 HH:MM - Step 1 - Initial creation.

"""
Configuration module for the YieldFi AI Agent.

This module provides access to the application's configuration settings,
loaded from config.yaml and environment variables.

Functions:
    load_config: Loads or reloads the configuration.
    get_config: Retrieves a specific configuration value.
"""

from .settings import get_config, load_config

__all__ = [
    'get_config',
    'load_config'
]

# src/config/__init__.py - Created 2025-05-07 

# Changelog:
# 2025-05-07 HH:MM - Step 5 - Confirmed load_config and get_config are exported.
# 2025-05-07 HH:MM - Step 1 - Initial creation. 