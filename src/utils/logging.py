"""
Logging utilities for the YieldFi AI Agent.

This module provides functions for setting up and managing application logging.
"""

import os
import logging
import datetime # Added for timestamp
from typing import Optional

from src.config.settings import get_config

LOG_DIRECTORY = "logs" # Define a constant for the logs directory

def setup_logging() -> None:
    """Set up logging for the application.
    
    Configures logging based on the application configuration.
    Logs will be written to a timestamped file in the 'logs' directory.
    """
    log_level_str = get_config('logging.level', 'INFO')
    log_level = getattr(logging, log_level_str.upper(), logging.INFO)
    
    # Ensure the main logs directory exists
    if not os.path.exists(LOG_DIRECTORY):
        os.makedirs(LOG_DIRECTORY)
        print(f"Created log directory: {LOG_DIRECTORY}") # For immediate feedback if run interactively
    
    # Generate a timestamped log file name
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    log_file_name = f"log-{timestamp}.log"
    log_file_path = os.path.join(LOG_DIRECTORY, log_file_name)
    
    # Configure logging
    # Remove basicConfig if we are setting up handlers manually
    # logging.basicConfig() can interfere if called multiple times or if handlers are added manually to root logger
    
    # Get the root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level) # Set level on root logger
    
    # Clear existing handlers from root logger (if any, to avoid duplication during re-runs/hot reloads)
    if root_logger.hasHandlers():
        root_logger.handlers.clear()

    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(module)s:%(lineno)d - %(message)s')

    # File Handler
    file_handler = logging.FileHandler(log_file_path)
    file_handler.setLevel(log_level) # Set level for file handler
    file_handler.setFormatter(formatter)
    root_logger.addHandler(file_handler)
    
    # Stream Handler (Console)
    stream_handler = logging.StreamHandler()
    # Console handler can have a different, potentially higher, level
    console_log_level_str = get_config('logging.console_level', log_level_str) # Allow separate console level
    console_log_level = getattr(logging, console_log_level_str.upper(), log_level)
    stream_handler.setLevel(console_log_level)
    stream_handler.setFormatter(formatter) # Can use a simpler formatter for console if desired
    root_logger.addHandler(stream_handler)
    
    # Set lower log level for external libraries
    logging.getLogger('urllib3').setLevel(logging.WARNING)
    logging.getLogger('tweepy').setLevel(logging.WARNING)
    
    # Log the configuration
    logger = get_logger('config') # This will now use the new setup
    logger.info('Logging configured. Level: %s. Console Level: %s. Log file: %s', 
                 log_level_str, console_log_level_str, log_file_path)
    logger.debug("This is a debug message from config logger to test setup.")


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