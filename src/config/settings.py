# Changelog:
# 2025-05-07 HH:MM - Step 5 - Clean implementation of configuration loading from YAML and .env.
# 2025-05-07 HH:MM - Step 20 (Fix) - Modified load_config to use _CONFIG_FILE_PATH for base, making DEFAULT_TEMPLATE a true fallback.
# 2025-05-07 HH:MM - Step 20 (Fix) - Normalize keys from .env to lowercase and improve os.environ override logic.

"""
Configuration settings for the YieldFi AI Agent.

This module provides functionality for loading and managing configuration settings
from environment variables and configuration files.
"""

import os
import yaml
from dotenv import load_dotenv
from typing import Any, Dict, Optional, Union
import copy # For deepcopy

# Global variable to store the loaded configuration
_CONFIG: Dict[str, Any] = {}
_CONFIG_LOADED = False

# Correctly determine project root and file paths
_PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
_CONFIG_FILE_PATH = os.path.join(_PROJECT_ROOT, "config.yaml") # This will be overridden by tests
_ENV_FILE_PATH = os.path.join(_PROJECT_ROOT, ".env")      # This will be overridden by tests

# Minimal default template, used if the primary config file is missing or invalid.
# The effective defaults for an application usually come from the config.yaml itself.
DEFAULT_TEMPLATE: Dict[str, Any] = {}

def _merge_dicts(target: Dict[str, Any], source: Dict[str, Any]) -> Dict[str, Any]:
    """Recursively merge two dictionaries, updating existing keys.
    
    Args:
        target: Target dictionary to update
        source: Source dictionary with values to merge
        
    Returns:
        The updated target dictionary
    """
    for key, value in source.items():
        if isinstance(value, dict) and key in target and isinstance(target[key], dict):
            _merge_dicts(target[key], value)
        else:
            target[key] = value
    
    return target

def _update_dict_from_env(config_dict: Dict[str, Any]) -> None:
    """
    Recursively updates the config dictionary with values from environment variables found 
    via load_dotenv. Keys are normalized to lowercase.
    Environment variables use double underscores for nesting: PARENT__CHILD__KEY=value
    """
    env_vars_to_process = os.environ.copy() # Work on a copy

    for env_key, env_value in env_vars_to_process.items():
        # Normalize parts to lowercase to match typical YAML conventions
        parts = [part.lower() for part in env_key.split('__')]
        
        current_level = config_dict
        for i, part in enumerate(parts):
            if i == len(parts) - 1: # Last part is the value
                # Try to convert to int/float/bool if possible, otherwise keep as string
                if env_value.lower() == 'true':
                    processed_value = True
                elif env_value.lower() == 'false':
                    processed_value = False
                elif env_value.isdigit():
                    processed_value = int(env_value)
                else:
                    try:
                        processed_value = float(env_value)
                    except ValueError:
                        processed_value = env_value # Keep as string
                
                current_level[part] = processed_value # Set with lowercase key
            else:
                # Ensure we are traversing into a dictionary, creating if necessary
                if part not in current_level or not isinstance(current_level[part], dict):
                    current_level[part] = {} # Create/overwrite with dict if needed
                current_level = current_level[part]
                # Check again if it's actually a dict after setdefault/creation attempt
                if not isinstance(current_level, dict):
                    # This path might have conflicted with a non-dict value earlier
                    # print(f"Warning: Env var {env_key} path conflicts at '{part}'. Skipping override.")
                    break 

def load_config() -> Dict[str, Any]:
    """Loads configuration from YAML file, then overrides with .env, then direct os.environ variables."""
    global _CONFIG, _CONFIG_LOADED

    # Determine base configuration from YAML file or use minimal default
    base_from_yaml: Dict[str, Any] = {}
    if os.path.exists(_CONFIG_FILE_PATH):
        try:
            with open(_CONFIG_FILE_PATH, 'r') as f:
                loaded_yaml = yaml.safe_load(f)
            if isinstance(loaded_yaml, dict) and loaded_yaml:
                base_from_yaml = loaded_yaml
            elif loaded_yaml is None: 
                print(f"Warning: Config file '{_CONFIG_FILE_PATH}' is empty. Using minimal defaults.")
                base_from_yaml = copy.deepcopy(DEFAULT_TEMPLATE) 
            else:
                print(f"Warning: Config file '{_CONFIG_FILE_PATH}' does not contain a valid YAML dictionary. Using minimal defaults.")
                base_from_yaml = copy.deepcopy(DEFAULT_TEMPLATE)
        except yaml.YAMLError as e:
            print(f"Error loading config file {_CONFIG_FILE_PATH}: Unable to parse YAML. {e}. Using minimal defaults.")
            base_from_yaml = copy.deepcopy(DEFAULT_TEMPLATE)
        except Exception as e:
            print(f"Error reading config file {_CONFIG_FILE_PATH}: {e}. Using minimal defaults.")
            base_from_yaml = copy.deepcopy(DEFAULT_TEMPLATE)
    else:
        print(f"Warning: Configuration file '{_CONFIG_FILE_PATH}' not found. Using minimal defaults and environment variables.")
        base_from_yaml = copy.deepcopy(DEFAULT_TEMPLATE)

    _CONFIG = base_from_yaml # Start with the loaded YAML or minimal default

    # Load .env file into os.environ.
    load_dotenv(dotenv_path=_ENV_FILE_PATH)

    # Override with values from .env (normalizing keys to lowercase)
    _update_dict_from_env(_CONFIG) 

    # Apply direct os.environ overrides (e.g., LOG_LEVEL=INFO from Docker/CI)
    # Normalize keys from os.environ to lowercase for consistent override behavior.
    # This assumes direct os.environ variables generally don't use __ for nesting.
    for env_key, env_value in os.environ.items():
        config_key = env_key.lower()
        if config_key in _CONFIG:
             # Try converting type similar to _update_dict_from_env
             if env_value.lower() == 'true':
                 processed_value = True
             elif env_value.lower() == 'false':
                 processed_value = False
             elif env_value.isdigit():
                 processed_value = int(env_value)
             else:
                 try:
                     processed_value = float(env_value)
                 except ValueError:
                     processed_value = env_value
             
             # Override only if the target isn't a dictionary (avoid replacing nested structures)
             if not isinstance(_CONFIG[config_key], dict):
                 _CONFIG[config_key] = processed_value
             # If _CONFIG[config_key] IS a dict, we don't override the whole dict with a flat env var.
             # Nested overrides should come from .env via __ convention handled by _update_dict_from_env.
        # Option: Add env vars as new top-level keys if they don't exist? 
        # else:
        #     _CONFIG[config_key] = processed_value # Add as new key

    _CONFIG_LOADED = True
    return copy.deepcopy(_CONFIG)

def get_config(key_path: str, default: Any = None) -> Any:
    """
    Retrieves a configuration value using a dot-separated key path (case-insensitive).
    If the configuration is not loaded, it will be loaded first.

    Args:
        key_path: Dot-separated path (e.g., 'ai.provider', case-insensitive).
        default: Default value to return if the key is not found.

    Returns:
        The configuration value or the default.
    """
    global _CONFIG_LOADED, _CONFIG
    if not _CONFIG_LOADED:
        load_config()
    
    # Use lowercase keys for retrieval to match normalization
    keys = key_path.lower().split('.')
    current_level = _CONFIG
    for key in keys:
        # Dictionary key access should be case-sensitive if _CONFIG wasn't normalized,
        # but since we normalize on load from env, we primarily expect lowercase keys.
        # However, YAML could have mixed case. We should ideally normalize YAML keys too,
        # or perform case-insensitive lookup here.
        # Simple approach: try lowercase first, then original if needed?
        # For now, assuming keys are mostly lowercase due to env override normalization.
        
        # Let's refine: Check case-insensitively for dict keys
        found_key = None
        if isinstance(current_level, dict):
            for current_key in current_level:
                if current_key.lower() == key:
                    found_key = current_key
                    break
        
        if found_key is not None:
            current_level = current_level[found_key]
        else:
            # Add this debug print statement before returning default
            # if key_path.lower() == "ai.xai_api_key":
            #     print(f"DEBUG: get_config for 'ai.xai_api_key' - key '{key}' not found in current_level. Returning default: {default}")
            return default # Key not found at this level
            
    # Add this debug print statement before the final return
    # if key_path.lower() == "ai.xai_api_key":
    #     print(f"DEBUG: get_config for 'ai.xai_api_key' is returning: {current_level}")

    if isinstance(current_level, (dict, list)):
        return copy.deepcopy(current_level)
    return current_level

# Removed automatic load_config() on import

def set_config_value(key: str, value: Any) -> None:
    """Sets a configuration value using dot notation (for testing/runtime changes)."""
    global _CONFIG, _CONFIG_LOADED
    if not _CONFIG_LOADED:
        load_config()
        
    keys = key.lower().split('.') # Use lowercase keys
    d = _CONFIG
    for part in keys[:-1]:
        if part not in d or not isinstance(d[part], dict):
            d[part] = {}
        d = d[part]
    d[keys[-1]] = value

def get_protocol_path(*parts: str) -> str:
    """
    Constructs a file path for protocol-specific resources.
    
    Args:
        *parts: Path parts to append to the protocol base directory
        
    Returns:
        Full path to the protocol resource
        
    Example:
        get_protocol_path("knowledge", "knowledge.json") will return
        something like "/path/to/data/protocols/ethena/knowledge/knowledge.json"
    """
    protocol = get_config("default_protocol", "ethena").lower()
    
    # Determine base protocols directory
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../'))
    protocol_dir = os.path.join(base_dir, "data", "protocols", protocol)
    
    # Check if protocol directory exists, if not log warning
    if not os.path.exists(protocol_dir):
        print(f"Warning: Protocol directory {protocol_dir} does not exist. Using default directory structure.")
        # Optional: fall back to non-protocol paths
    
    # Construct path with provided parts
    return os.path.join(protocol_dir, *parts)

# Removed automatic load_config() on import

# Default protocol setting, used throughout the app
DEFAULT_PROTOCOL = get_config("protocols.default_protocol", "yieldfi")

# Export publicly
__all__ = ['get_config', 'load_config', 'set_config_value', 'get_protocol_path', 'DEFAULT_PROTOCOL'] 