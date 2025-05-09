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
        self.xai_model = get_config("ai.xai_model", "grok-3-mini-beta")
        self.google_palm_base_url = get_config("ai.google_palm_base_url", "https://generativelanguage.googleapis.com/v1beta")
        
        self.default_max_tokens = get_config("ai.default_max_tokens", 1500)
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
        logger.info(f"XAIClient.get_completion called. Prompt (first 500 chars): '{prompt[:500]}...'")
        logger.debug(f"Params: max_tokens={current_max_tokens}, temperature={current_temperature}, other_kwargs={kwargs}")
        
        use_xai_api = bool(self.xai_api_key) and not self.use_fallback
        use_google_api = bool(self.google_api_key) and (self.use_fallback or not bool(self.xai_api_key))

        try:
            if use_xai_api:
                logger.info(f"Attempting to call xAI API. Endpoint: {self.xai_base_url}/completions, Model: {self.xai_model}")
                # Construct the payload for xAI completions
                payload = {
                    "prompt": prompt,
                    "model": self.xai_model,
                    "max_tokens": current_max_tokens,
                    "temperature": current_temperature,
                    **kwargs
                }
                headers["Authorization"] = f"Bearer {self.xai_api_key}"
                logger.debug(f"xAI API Request Payload (excluding Authorization header): {payload}")
                
                # Log the exact prompt being sent to identify potential pattern issues
                prompt_len = len(prompt)
                prompt_first_100 = prompt[:100] if prompt_len > 0 else 'empty'
                prompt_last_100 = prompt[-100:] if prompt_len > 100 else prompt
                logger.info(f"Sending to xAI API: prompt length={prompt_len}, first 100 chars='{prompt_first_100}...', last 100 chars='...{prompt_last_100}'")
                
                # Make the API request
                response = requests.post(f"{self.xai_base_url}/completions", json=payload, headers=headers, timeout=30)
                logger.info(f"xAI API raw response status: {response.status_code}")
                
                # Debug the raw response
                response_text = response.text
                logger.debug(f"xAI API raw response text: {response_text}")
                response.raise_for_status()
                
                # Parse and debug the JSON response
                json_response = response.json()
                logger.debug(f"xAI API parsed JSON response: {json_response}")
                
                # Check for potential echo issues in the response
                self._check_for_echo(prompt, json_response)
                
                return json_response
            
            elif use_google_api:
                logger.info(f"Attempting to call Google PaLM API. Fallback active or xAI key missing. Using model: text-bison-001 (example)")
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
                logger.debug(f"Google PaLM API Request URL: {palm_api_url}")
                logger.debug(f"Google PaLM API Request Payload: {palm_payload}")
                
                response = requests.post(palm_api_url, json=palm_payload, headers=headers, timeout=30)
                logger.info(f"Google PaLM API raw response status: {response.status_code}")
                logger.debug(f"Google PaLM API raw response text: {response.text}")
                response.raise_for_status()
                json_response = response.json()
                logger.debug(f"Google PaLM API parsed JSON response: {json_response}")
                return json_response

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
            
    def _check_for_echo(self, prompt: str, response: Dict[str, Any]) -> None:
        """Check if the response appears to be echoing the prompt.
        
        Args:
            prompt: The original prompt sent to the API
            response: The parsed JSON response from the API
        """
        # Skip if response is not in expected format
        if not isinstance(response, dict):
            logger.warning(f"Cannot check for echo: response is not a dictionary")
            return
            
        # Extract response text from various possible formats
        response_text = None
        if 'choices' in response and isinstance(response['choices'], list) and len(response['choices']) > 0:
            choice = response['choices'][0]
            if isinstance(choice, dict):
                if 'text' in choice:
                    response_text = choice['text']
                elif 'message' in choice and isinstance(choice['message'], dict) and 'content' in choice['message']:
                    response_text = choice['message']['content']
        elif 'candidates' in response and isinstance(response['candidates'], list) and len(response['candidates']) > 0:
            candidate = response['candidates'][0]
            if isinstance(candidate, dict) and 'output' in candidate:
                response_text = candidate['output']
                
        if not response_text:
            logger.warning("Could not extract response text for echo checking")
            return
            
        # Check for exact echo - highly suspicious
        if prompt.strip() == response_text.strip():
            logger.critical(f"CRITICAL: API returned the exact prompt as the response - 100% match!")
            return
            
        # Check for high similarity - might be partial echo
        prompt_stripped = prompt.strip().lower()
        response_stripped = response_text.strip().lower()
        
        # Check if response is contained in prompt
        if len(response_stripped) > 10 and response_stripped in prompt_stripped:
            coverage = (len(response_stripped) / len(prompt_stripped)) * 100 if len(prompt_stripped) > 0 else 0
            logger.error(f"SUSPICIOUS: Response text appears to be a subset of the prompt ({coverage:.1f}% coverage)")
            
        # Check if prompt is contained in response (common for instruct models to repeat instructions)
        elif len(prompt_stripped) > 10 and prompt_stripped in response_stripped:
            coverage = (len(prompt_stripped) / len(response_stripped)) * 100 if len(response_stripped) > 0 else 0
            if coverage > 80:  # If prompt makes up over 80% of response, likely echo
                logger.error(f"SUSPICIOUS: Response contains most of the prompt ({coverage:.1f}% coverage)")
            else:
                logger.warning(f"Response contains part of the prompt ({coverage:.1f}% coverage) - this may be normal instruction repetition")
                
        # Quick check for first/last line matches
        prompt_lines = prompt_stripped.split('\n')
        response_lines = response_stripped.split('\n')
        
        if prompt_lines and response_lines:
            if prompt_lines[-1] == response_lines[0]:
                logger.warning("First line of response matches last line of prompt - possible continuation issue")
                
        logger.debug(f"Echo check complete: prompt={len(prompt_stripped)} chars, response={len(response_stripped)} chars")

# Helper for the JSON error response test if MESSAGE_KEY is used in XAIClient for extracting error messages from JSON.
# If not, the literal string 'message' should be used in the assertEqual.
MESSAGE_KEY = 'message' # Or whatever key the actual XAI client uses for the error message in JSON 

# Debug helpers
def extract_responses(raw_json_response: Dict[str, Any]) -> List[str]:
    """Extract all possible response texts from an API response for debugging.
    
    Args:
        raw_json_response: The parsed JSON response from an AI API
        
    Returns:
        A list of extracted texts from the response
    """
    texts = []
    
    # Try to extract from all common response formats
    if not isinstance(raw_json_response, dict):
        return [str(raw_json_response)]
        
    # Extract from 'choices' format (OpenAI, xAI)
    if 'choices' in raw_json_response and isinstance(raw_json_response['choices'], list):
        for choice in raw_json_response['choices']:
            if not isinstance(choice, dict):
                continue
                
            # Text completion format
            if 'text' in choice:
                texts.append(choice['text'])
                
            # Chat completion format
            if 'message' in choice and isinstance(choice['message'], dict):
                if 'content' in choice['message']:
                    texts.append(choice['message']['content'])
                    
            # Reasoning format sometimes used
            if 'reasoning_content' in choice:
                texts.append(choice['reasoning_content'])
                
    # Extract from 'candidates' format (PaLM, Gemini, etc)
    if 'candidates' in raw_json_response and isinstance(raw_json_response['candidates'], list):
        for candidate in raw_json_response['candidates']:
            if not isinstance(candidate, dict):
                continue
                
            if 'output' in candidate:
                texts.append(candidate['output'])
                
            if 'content' in candidate:
                texts.append(candidate['content'])
                
    # Extract from 'response' key (less common)
    if 'response' in raw_json_response:
        if isinstance(raw_json_response['response'], str):
            texts.append(raw_json_response['response'])
            
    # Extract from 'text' key (less common)
    if 'text' in raw_json_response:
        if isinstance(raw_json_response['text'], str):
            texts.append(raw_json_response['text'])
            
    return texts