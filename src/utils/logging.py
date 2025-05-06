"""
Logging utilities for the YieldFi AI Agent.

This module provides functions for setting up and managing application logging.
"""

import os
import logging
from typing import Optional

from src.config.settings import get_config


def setup_logging() -> None:
    """Set up logging for the application.
    
    Configures logging based on the application configuration.
    """
    log_level_str = get_config('logging.level', 'INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    log_file = get_config('logging.file', 'yieldfi_ai_agent.log')
    
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
    
    # Set lower log level for external libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('tweepy').setLevel(logging.WARNING)
    
    # Log the configuration
    logger = get_logger('config')
    logger.debug('Logging configured with level %s', log_level_str)


def get_logger(name: Optional[str] = None) -> logging.Logger:
    """Get a logger instance.
    
    Args:
        name: Name of the logger (typically the module name)
        
    Returns:
        Logger instance
    """
    if name is None:
        return logging.getLogger()
    
    # Prepend the application name to the logger name
    app_name = get_config('app.name', 'YieldFi AI Agent').replace(' ', '_').lower()
    return logging.getLogger(f"{app_name}.{name}") 