# Changelog:
# 2025-05-07 HH:MM - Step 5 - Validated existing configuration system. Confirmed loading from YAML and .env, dot-notation access via get_config, and env var precedence.

"""
Configuration settings for the YieldFi AI Agent.

This module provides functionality for loading and managing configuration settings
from environment variables and configuration files.
"""

import os
import yaml
from typing import Any, Dict, Optional
from dotenv import load_dotenv

# Global configuration object
_config = {}


def load_config(config_file: str = 'config.yaml') -> Dict[str, Any]:
    """Load configuration from environment variables and config file.
    
    Args:
        config_file: Path to the YAML configuration file
        
    Returns:
        Dictionary containing the configuration settings
    """
    global _config
    
    # Load environment variables from .env file
    load_dotenv()
    
    # Default configuration
    config = {
        'app': {
            'name': 'YieldFi AI Agent',
            'version': '0.1.0',
            'debug': False,
        },
        'data_source': {
            'type': 'mock',  # Default to mock data source for development
            'twitter': {
                'bearer_token': os.environ.get('TWITTER_BEARER_TOKEN', ''),
                'api_key': os.environ.get('TWITTER_API_KEY', ''),
                'api_secret': os.environ.get('TWITTER_API_SECRET', ''),
                'access_token': os.environ.get('TWITTER_ACCESS_TOKEN', ''),
                'access_token_secret': os.environ.get('TWITTER_ACCESS_TOKEN_SECRET', ''),
            }
        },
        'ai': {
            'provider': 'xai',
            'xai_api_key': os.environ.get('XAI_API_KEY', ''),
            'fallback_provider': 'google_palm',
            'google_palm_api_key': os.environ.get('GOOGLE_API_KEY', ''),
            'max_tokens': 1000,
            'temperature': 0.7,
        },
        'tweet_categories': [
            'announcement',
            'product-updates',
            'community-updates',
            'events',
            'yieldfi-security',
            'yieldfi-transparency',
        ],
        'tone_analysis': {
            'enabled': True,
            'method': 'textblob',  # Options: 'textblob', 'xai', 'google_palm'
        },
        'logging': {
            'level': 'INFO',
            'file': 'yieldfi_ai_agent.log',
        },
        'ui': {
            'theme': 'light',
            'show_debug_info': False,
        },
        'data_paths': {
            'input': 'data/input',
            'output': 'data/output',
            'knowledge': 'data/docs',
        }
    }
    
    # Load config from file if it exists
    if os.path.exists(config_file):
        try:
            with open(config_file, 'r') as f:
                file_config = yaml.safe_load(f)
                if file_config:  # Ensure file_config is not None (e.g. empty file)
                    _merge_dicts(config, file_config)
        except yaml.YAMLError as e: # Catch specific YAML parsing errors
            print(f"Error loading config file {config_file}: Unable to parse YAML.")
        except Exception as e:
            print(f"Error loading config file {config_file}: {e}")
    
    # Override with environment variables
    if os.environ.get('DEBUG') == 'true':
        config['app']['debug'] = True
    
    if os.environ.get('LOG_LEVEL'):
        config['logging']['level'] = os.environ.get('LOG_LEVEL')
    
    if os.environ.get('DATA_SOURCE_TYPE'):
        config['data_source']['type'] = os.environ.get('DATA_SOURCE_TYPE')
    
    _config = config
    return config


def get_config(key: Optional[str] = None, default: Any = None) -> Any:
    """Get a configuration value.
    
    Args:
        key: Dot-separated path to the configuration value (e.g., 'app.debug')
            If None, returns the entire configuration
        default: Default value to return if the key is not found
        
    Returns:
        The configuration value or the default value if not found
    """
    if not _config:
        load_config()
    
    if key is None:
        return _config
    
    # Navigate the nested dictionary using the dot-separated path
    value = _config
    for part in key.split('.'):
        if isinstance(value, dict) and part in value:
            value = value[part]
        else:
            return default
    
    return value


def set_config_value(key: str, value: Any) -> None:
    """Set a configuration value.
    
    Args:
        key: Dot-separated path to the configuration value (e.g., 'app.debug')
        value: Value to set
    """
    if not _config:
        load_config()
    
    # Navigate the nested dictionary using the dot-separated path
    parts = key.split('.')
    config = _config
    
    # Navigate to the parent of the target key
    for part in parts[:-1]:
        if part not in config:
            config[part] = {}
        config = config[part]
    
    # Set the value
    config[parts[-1]] = value


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