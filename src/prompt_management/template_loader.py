# Changelog:
# 2025-05-09 18:15 - Step 408 - Created template_loader for centralized prompt management.

"""
Template loader for managing prompt templates.

This module provides functionality to load prompt templates from JSON files,
cache them for performance, and access different components of the templates
based on the selected protocol.
"""

import os
import json
from enum import Enum
from typing import Any, Dict, List, Optional, Union
from pathlib import Path

# Logger instance
from src.utils.logging import get_logger
logger = get_logger(__name__)


class PromptKey(Enum):
    """Enum for standard keys in prompt templates for consistent access."""
    BASE_INSTRUCTIONS = "base_instructions"
    PERSONA = "persona"
    CORE_MESSAGE = "core_message"
    INTERACTION_MODES = "interaction_modes"
    RESPONSE_PREFIX = "response_prefix"
    INSTRUCTION_SETS = "instruction_sets"
    CRITICAL_INSTRUCTIONS = "critical_instructions"
    FALLBACKS = "fallbacks"


class PromptTemplate:
    """
    Manages loading and access to prompt templates from JSON files.
    
    This class implements the Singleton pattern to ensure template caching
    and consistent access across the application.
    """
    _instance = None
    _templates: Dict[str, Dict[str, Any]] = {}
    _default_protocol: str = "yieldfi"  # Default fallback

    def __new__(cls):
        """Singleton pattern implementation."""
        if cls._instance is None:
            cls._instance = super(PromptTemplate, cls).__new__(cls)
            # Initialize instance attributes
            cls._instance._templates = {}
            # Try to get default protocol from settings
            try:
                from src.config.settings import get_config
                cls._instance._default_protocol = get_config("DEFAULT_PROTOCOL", "yieldfi")
            except (ImportError, AttributeError):
                logger.warning("Could not load DEFAULT_PROTOCOL from settings, using fallback: yieldfi")
        return cls._instance

    @classmethod
    def _get_protocol_path(cls, protocol_name: str) -> str:
        """
        Get the path to a protocol's prompt templates file.
        
        Args:
            protocol_name: The name of the protocol.
            
        Returns:
            The path to the protocol's prompt templates file.
        """
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'protocols'))
        return os.path.join(base_dir, protocol_name, 'prompt_templates.json')

    @classmethod
    def load_template(cls, protocol_name: str = None) -> Dict[str, Any]:
        """
        Load a prompt template for a specific protocol.
        
        Args:
            protocol_name: The name of the protocol to load.
                          If None, uses the default protocol.
                          
        Returns:
            The loaded template as a dictionary.
        """
        # Use default if not specified
        if protocol_name is None:
            protocol_name = cls._default_protocol
            
        # Return cached template if available
        if protocol_name in cls._templates:
            return cls._templates[protocol_name]
            
        # Load template from file
        template_path = cls._get_protocol_path(protocol_name)
        try:
            if not os.path.exists(template_path):
                logger.warning(f"Template file not found for protocol '{protocol_name}' at {template_path}. "
                               f"Falling back to default protocol: {cls._default_protocol}")
                
                # If protocol not found and it's not already the default, try loading the default
                if protocol_name != cls._default_protocol:
                    return cls.load_template(cls._default_protocol)
                    
                # If it is the default that's missing, we have a bigger problem
                logger.error(f"Default protocol template not found at {template_path}.")
                return {}
                
            with open(template_path, 'r') as f:
                template = json.load(f)
                cls._templates[protocol_name] = template
                logger.info(f"Loaded template for protocol: {protocol_name}")
                return template
                
        except Exception as e:
            logger.error(f"Error loading template for protocol '{protocol_name}': {e}")
            # If this wasn't the default protocol, try loading the default
            if protocol_name != cls._default_protocol:
                logger.warning(f"Falling back to default protocol: {cls._default_protocol}")
                return cls.load_template(cls._default_protocol)
            return {}

    @classmethod
    def get(cls, key: Union[str, PromptKey], protocol_name: Optional[str] = None, 
            *sub_keys: str, default: Any = None) -> Any:
        """
        Get a value from a prompt template.
        
        Args:
            key: The key to access in the template. Can be a string or PromptKey enum.
            protocol_name: The protocol name to load the template for.
                          If None, uses the default protocol.
            *sub_keys: Optional subkeys for nested access.
            default: Default value if the key or subkeys are not found.
            
        Returns:
            The value from the template or the default if not found.
        """
        # Convert PromptKey enum to string if needed
        if isinstance(key, PromptKey):
            key = key.value
            
        # Load template if not already loaded
        template = cls.load_template(protocol_name)
        
        # Get base value from template
        value = template.get(key)
        if value is None:
            # Try to get fallback from template
            fallbacks = template.get('fallbacks', {})
            value = fallbacks.get(key, default)
            
        # Process subkeys for nested access
        for sub_key in sub_keys:
            if isinstance(value, dict) and sub_key in value:
                value = value.get(sub_key)
            else:
                # If any subkey is missing, return default
                return default
                
        return value if value is not None else default

    @classmethod
    def get_persona(cls, account_type: str, protocol_name: Optional[str] = None, 
                    default: str = None) -> str:
        """
        Get a persona description for a specific account type.
        
        Args:
            account_type: The account type (e.g., 'OFFICIAL', 'INTERN').
            protocol_name: The protocol name.
            default: Default persona if not found.
            
        Returns:
            The persona description as a string.
        """
        persona = cls.get(PromptKey.PERSONA, protocol_name, default={})
        return persona.get(account_type, default or cls.get(
            PromptKey.FALLBACKS, protocol_name, 'persona', default=""))

    @classmethod
    def get_interaction_mode(cls, mode: str, protocol_name: Optional[str] = None) -> Dict[str, Any]:
        """
        Get interaction mode details.
        
        Args:
            mode: The interaction mode (e.g., 'DEFAULT', 'PROFESSIONAL').
            protocol_name: The protocol name.
            
        Returns:
            A dictionary with mode details.
        """
        interaction_modes = cls.get(PromptKey.INTERACTION_MODES, protocol_name, default={})
        mode_upper = mode.upper() if isinstance(mode, str) else "DEFAULT"
        return interaction_modes.get(mode_upper, 
                                     cls.get(PromptKey.FALLBACKS, protocol_name, 'interaction_mode', default={}))

    @classmethod
    def get_instruction_set(cls, active_type: str, target_type: str, 
                           protocol_name: Optional[str] = None, default: str = None) -> str:
        """
        Get instruction set for specific account type interaction.
        
        Args:
            active_type: The active account type.
            target_type: The target account type.
            protocol_name: The protocol name.
            default: Default instruction set if not found.
            
        Returns:
            The instruction set as a string.
        """
        key = f"{active_type}_TO_{target_type}"
        instruction_sets = cls.get(PromptKey.INSTRUCTION_SETS, protocol_name, default={})
        return instruction_sets.get(key, default or cls.get(
            PromptKey.FALLBACKS, protocol_name, 'instruction_set', default=""))

    @classmethod
    def get_critical_instructions(cls, platform: str, protocol_name: Optional[str] = None) -> List[str]:
        """
        Get critical instructions for a specific platform.
        
        Args:
            platform: The platform (e.g., 'twitter').
            protocol_name: The protocol name.
            
        Returns:
            A list of critical instructions.
        """
        critical_instr = cls.get(PromptKey.CRITICAL_INSTRUCTIONS, protocol_name, default={})
        platform_lower = platform.lower() if isinstance(platform, str) else "twitter"
        return critical_instr.get(platform_lower, [])
