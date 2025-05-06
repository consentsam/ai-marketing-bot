"""
Error handling utilities for the YieldFi AI Agent.

This module provides functions and classes for managing API errors and exceptions.
"""

import functools
import traceback
from typing import Any, Callable, Dict, Optional, TypeVar, cast

from src.utils.logging import get_logger

# Logger instance
logger = get_logger('error_handling')

# Type variable for functions
F = TypeVar('F', bound=Callable[..., Any])


class APIError(Exception):
    """Exception raised for API errors.
    
    Attributes:
        status_code: HTTP status code or error code
        message: Error message
        details: Additional error details
    """
    
    def __init__(
        self, 
        message: str, 
        status_code: Optional[int] = None,
        details: Optional[Dict[str, Any]] = None
    ):
        """Initialize the APIError.
        
        Args:
            message: Error message
            status_code: HTTP status code or error code
            details: Additional error details
        """
        self.status_code = status_code
        self.message = message
        self.details = details or {}
        super().__init__(message)


def handle_api_error(func: F) -> F:
    """Decorator to handle API errors.
    
    This decorator catches exceptions, logs them, and returns a standardized error response.
    
    Args:
        func: Function to decorate
        
    Returns:
        Decorated function
    """
    @functools.wraps(func)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
        try:
            return func(*args, **kwargs)
        except APIError as e:
            logger.error(
                "API Error: %s (status code: %s, details: %s)",
                e.message,
                e.status_code,
                e.details
            )
            return {
                'error': True,
                'message': e.message,
                'status_code': e.status_code,
                'details': e.details
            }
        except Exception as e:
            logger.error("Unexpected error: %s", str(e))
            logger.debug(traceback.format_exc())
            return {
                'error': True,
                'message': str(e),
                'status_code': 500,
                'details': {'traceback': traceback.format_exc()}
            }
    
    return cast(F, wrapper) 