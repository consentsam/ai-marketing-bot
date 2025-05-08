"""
xAI API client for the YieldFi AI Agent.

This module provides a client for interacting with the xAI API for generating responses.
In the future, this will be replaced with the actual xAI API client when it's available.
"""

import requests
import os
from typing import Dict, Any, List, Optional

# Attempt to import get_config from src.config, then src.config.settings as a fallback for flexibility
try:
    from src.config import get_config
except ImportError:
    from src.config.settings import get_config

from src.utils.logging import get_logger
from src.utils.error_handling import APIError, handle_api_error

# Logger instance
logger = get_logger('xai_client')


class XAIClient:
    """
    Client for interacting with the xAI API (mocked) with a fallback to Google PaLM (mocked).
    Retrieves API keys and settings from the configuration system.
    """

    def __init__(
        self,
        api_key: Optional[str] = None,
        google_api_key: Optional[str] = None
    ):
        """
        Initializes the XAIClient.

        Args:
            api_key: The xAI API key. If None, attempts to load from config 'ai.xai_api_key'.
            google_api_key: The Google API key. If None, attempts to load from config 'ai.google_api_key'.
        """
        self.xai_api_key = api_key or get_config("ai.xai_api_key")
        self.google_api_key = google_api_key or get_config("ai.google_api_key")
        
        self.use_fallback = get_config("ai.use_fallback", False)
        
        self.xai_base_url = get_config("ai.xai_base_url", "https://api.x.ai/v1")
        self.xai_model = get_config("ai.xai_model", "grok-3-latest")
        self.google_palm_base_url = get_config("ai.google_palm_base_url", "https://generativelanguage.googleapis.com/v1beta")
        
        self.default_max_tokens = get_config("ai.default_max_tokens", 150)
        self.default_temperature = get_config("ai.default_temperature", 0.7)

    def get_completion(
        self,
        prompt: str,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None,
        **kwargs: Any
    ) -> Dict[str, Any]:
        """
        Generates a text completion using either xAI or Google PaLM.
        Actual API calls will be made, relying on tests to mock 'requests.post'.

        Args:
            prompt: The prompt to send to the API.
            max_tokens: The maximum number of tokens to generate. Defaults to config value.
            temperature: The sampling temperature. Defaults to config value.
            **kwargs: Additional arguments for the API call.

        Returns:
            A dictionary containing the API response.

        Raises:
            APIError: If API call fails or no API is available.
        """
        current_max_tokens = max_tokens if max_tokens is not None else self.default_max_tokens
        current_temperature = temperature if temperature is not None else self.default_temperature

        headers = {"Content-Type": "application/json"}
        
        use_xai_api = bool(self.xai_api_key) and not self.use_fallback
        use_google_api = bool(self.google_api_key) and (self.use_fallback or not bool(self.xai_api_key))

        try:
            if use_xai_api:
                logger.info(f"Calling xAI API: {self.xai_base_url}/chat/completions")
                # Construct the messages payload for chat completions
                messages = [
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ]
                payload = {
                    "messages": messages,
                    "model": self.xai_model,
                    "max_tokens": current_max_tokens,
                    "temperature": current_temperature,
                    "stream": False,
                    **kwargs
                }
                headers["Authorization"] = f"Bearer {self.xai_api_key}"
                response = requests.post(f"{self.xai_base_url}/chat/completions", json=payload, headers=headers, timeout=30)
                response.raise_for_status() # Will raise HTTPError for bad responses (4xx or 5xx)
                return response.json()
            
            elif use_google_api:
                logger.info(f"Calling Google PaLM API: {self.google_palm_base_url}")
                # PaLM API structure can vary; this is a common pattern for older models
                # For newer Gemini via Vertex or AI Studio, the endpoint and payload would differ.
                # Assuming a text generation model like 'text-bison-001' for this example.
                palm_payload = {
                    "prompt": {
                        "text": prompt
                    },
                    # "temperature": current_temperature, # PaLM might have different ways to set this
                    # "maxOutputTokens": current_max_tokens,
                }
                # Add other PaLM specific params from kwargs if necessary
                # e.g., safetySettings, stopSequences

                # The actual model name might need to be part of the URL or payload
                # This is a generic example:
                palm_api_url = f"{self.google_palm_base_url}/models/text-bison-001:generateText?key={self.google_api_key}"
                
                response = requests.post(palm_api_url, json=palm_payload, headers=headers, timeout=30)
                response.raise_for_status()
                return response.json()

            else:
                # This case should ideally be caught by upfront config checks,
                # but it's a safeguard here.
                logger.error("No API available. Check configuration for xAI/Google API keys and fallback settings.")
                raise APIError(
                    "No API available. Check configuration for xAI/Google API keys and fallback settings.", 
                    status_code=503 # Service Unavailable
                )
        
        except requests.exceptions.HTTPError as e:
            status_code = e.response.status_code if e.response is not None else 500
            error_text = "Unknown HTTP error"
            details = {}
            if e.response is not None:
                error_text = e.response.text
                try:
                    details = e.response.json() # Attempt to get JSON error details
                    # If 'error' and 'message' keys exist, use that as a more specific message
                    if isinstance(details, dict) and 'error' in details and isinstance(details['error'], dict) and 'message' in details['error']:
                        error_text = details['error']['message']
                    elif isinstance(details, dict) and MESSAGE_KEY in details : # MESSAGE_KEY is 'message'
                         error_text = details[MESSAGE_KEY]

                except ValueError: # Not JSON
                    details = {"raw_response": error_text} # Keep raw text if not JSON
            
            logger.error(f"API request failed: {status_code} - {error_text}", exc_info=True)
            raise APIError(f"API request failed with status {status_code}: {error_text}", status_code=status_code, details=details) from e
        
        except requests.exceptions.RequestException as e: # Catches ConnectionError, Timeout, etc.
            logger.error(f"API request failed due to a network/connection issue: {e}", exc_info=True)
            raise APIError(f"API request failed due to a network/connection issue: {str(e)}", status_code=500) from e
        
        except Exception as e:
            # Catch any other unexpected error during the process
            logger.error(f"An unexpected error occurred in XAIClient.get_completion: {e}", exc_info=True)
            raise APIError(f"An unexpected error occurred in XAIClient.get_completion: {str(e)}", status_code=500) from e

# Helper for the JSON error response test if MESSAGE_KEY is used in XAIClient for extracting error messages from JSON.
# If not, the literal string 'message' should be used in the assertEqual.
MESSAGE_KEY = 'message' # Or whatever key the actual XAI client uses for the error message in JSON

# Helper for the JSON error response test if MESSAGE_KEY is used in XAIClient for extracting error messages from JSON.
# If not, the literal string 'message' should be used in the assertEqual.
MESSAGE_KEY = 'message' # Or whatever key the actual XAI client uses for the error message in JSON 