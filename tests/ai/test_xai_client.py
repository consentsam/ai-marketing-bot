# Changelog:
# 2025-05-07 HH:MM - Step 20 (Initial) - Added comprehensive tests for XAIClient.
# 2025-05-07 HH:MM - Step 20 (Fix) - Adjusted tests after XAIClient refactor to use mocked requests.post.

import unittest
from unittest.mock import patch, MagicMock
import os

# Ensure the test can find the src modules
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from src.ai.xai_client import XAIClient, MESSAGE_KEY # type: ignore
from src.utils.error_handling import APIError # type: ignore
import requests # For requests.exceptions

class TestXAIClient(unittest.TestCase):

    def setUp(self):
        """Reset environment variables and config mocks for each test."""
        self.env_vars_to_clear = [
            'AI__XAI_API_KEY', 'AI__GOOGLE_API_KEY', 'AI__USE_FALLBACK',
            'AI__XAI_BASE_URL', 'AI__GOOGLE_PALM_BASE_URL',
            'AI__DEFAULT_MAX_TOKENS', 'AI__DEFAULT_TEMPERATURE'
        ]
        for key in self.env_vars_to_clear:
            if key in os.environ:
                del os.environ[key]
        
        # Default mock config values
        self.mock_config_values = {
            "ai.xai_api_key": "test_xai_key",
            "ai.google_api_key": "test_google_key",
            "ai.use_fallback": False,
            "ai.xai_base_url": "mock://xai.com",
            "ai.google_palm_base_url": "mock://google.com",
            "ai.default_max_tokens": 100,
            "ai.default_temperature": 0.5
        }

    def tearDown(self):
        """Clean up environment variables after each test."""
        for key in self.env_vars_to_clear:
            if key in os.environ:
                del os.environ[key]

    @patch('src.ai.xai_client.get_config')
    def test_init_loads_keys_from_config(self, mock_get_config):
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)
        
        client = XAIClient()
        self.assertEqual(client.xai_api_key, "test_xai_key")
        self.assertEqual(client.google_api_key, "test_google_key")
        self.assertFalse(client.use_fallback)
        self.assertEqual(client.xai_base_url, "mock://xai.com")
        self.assertEqual(client.google_palm_base_url, "mock://google.com")
        self.assertEqual(client.default_max_tokens, 100)
        self.assertEqual(client.default_temperature, 0.5)

    @patch('src.ai.xai_client.get_config')
    def test_init_with_direct_keys(self, mock_get_config):
        # Ensure get_config is not called for api_key if provided directly
        # but is called for other settings like use_fallback
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)
        client = XAIClient(api_key="direct_xai", google_api_key="direct_google")
        self.assertEqual(client.xai_api_key, "direct_xai")
        self.assertEqual(client.google_api_key, "direct_google")
        
        # Check that get_config was called for other non-provided settings
        # Example: ai.use_fallback
        found_use_fallback_call = False
        for call_args in mock_get_config.call_args_list:
            if call_args[0][0] == "ai.use_fallback":
                found_use_fallback_call = True
                break
        self.assertTrue(found_use_fallback_call, "get_config should have been called for ai.use_fallback")

    @patch('src.ai.xai_client.requests.post')
    @patch('src.ai.xai_client.get_config')
    def test_get_completion_xai_success(self, mock_get_config, mock_post):
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)
        
        expected_response_json = {"choices": [{"text": "xAI actual response"}]}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response_json
        mock_post.return_value = mock_response
        
        client = XAIClient()
        prompt_text = "Hello xAI"
        response = client.get_completion(prompt_text)
        
        self.assertEqual(response, expected_response_json)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertEqual(args[0], "mock://xai.com/completions")
        self.assertEqual(kwargs['json']['prompt'], prompt_text)
        self.assertEqual(kwargs['headers']['Authorization'], "Bearer test_xai_key")

    @patch('src.ai.xai_client.requests.post')
    @patch('src.ai.xai_client.get_config')
    def test_get_completion_google_fallback_when_xai_key_missing(self, mock_get_config, mock_post):
        self.mock_config_values["ai.xai_api_key"] = None # Simulate missing xAI key
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)

        expected_response_json = {"candidates": [{"output": "Google actual response"}]}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response_json
        mock_post.return_value = mock_response
        
        client = XAIClient()
        prompt_text = "Hello Google"
        response = client.get_completion(prompt_text)
        
        self.assertEqual(response, expected_response_json)
        mock_post.assert_called_once()
        args, kwargs = mock_post.call_args
        self.assertTrue(args[0].startswith("mock://google.com/models/text-bison-001:generateText"))
        self.assertIn("test_google_key", args[0]) # Key in URL for PaLM
        self.assertEqual(kwargs['json']['prompt']['text'], prompt_text)

    @patch('src.ai.xai_client.requests.post')
    @patch('src.ai.xai_client.get_config')
    def test_get_completion_google_fallback_when_use_fallback_true(self, mock_get_config, mock_post):
        self.mock_config_values["ai.use_fallback"] = True # Force fallback
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)

        expected_response_json = {"candidates": [{"output": "Google forced fallback actual"}]}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response_json
        mock_post.return_value = mock_response
        
        client = XAIClient()
        response = client.get_completion("Test prompt")
        self.assertEqual(response, expected_response_json)
        self.assertTrue(mock_post.call_args[0][0].startswith("mock://google.com"))

    @patch('src.ai.xai_client.get_config')
    def test_get_completion_no_api_key_available(self, mock_get_config):
        self.mock_config_values["ai.xai_api_key"] = None
        self.mock_config_values["ai.google_api_key"] = None
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)
        
        client = XAIClient()
        with self.assertRaisesRegex(APIError, "No API available"): 
            client.get_completion("Test prompt")

    @patch('src.ai.xai_client.requests.post')
    @patch('src.ai.xai_client.get_config')
    def test_get_completion_xai_http_error(self, mock_get_config, mock_post):
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)
        
        mock_err_response = MagicMock()
        mock_err_response.status_code = 401
        mock_err_response.text = "Unauthorized text"
        mock_err_response.json.side_effect = ValueError # Simulate non-JSON error response text
        
        # Configure the mock_post to raise an HTTPError with the mock_err_response
        mock_post.side_effect = requests.exceptions.HTTPError(response=mock_err_response)
        
        client = XAIClient()
        with self.assertRaisesRegex(APIError, "API request failed with status 401: Unauthorized text") as cm:
            client.get_completion("Test prompt")
        self.assertEqual(cm.exception.status_code, 401)
        self.assertEqual(cm.exception.details, {"raw_response": "Unauthorized text"})

    @patch('src.ai.xai_client.requests.post')
    @patch('src.ai.xai_client.get_config')
    def test_get_completion_xai_http_error_with_json_response(self, mock_get_config, mock_post):
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)
        
        mock_err_response = MagicMock()
        mock_err_response.status_code = 429
        # The error message is now extracted from the JSON if possible
        error_json_payload = {"error": {"message": "Rate limit exceeded from JSON"}}
        mock_err_response.json.return_value = error_json_payload
        mock_err_response.text = str(error_json_payload) # text might still be accessed by some part of requests
        mock_post.side_effect = requests.exceptions.HTTPError(response=mock_err_response)
        
        client = XAIClient()
        # The error message in APIError should now be "Rate limit exceeded from JSON"
        with self.assertRaisesRegex(APIError, "API request failed with status 429: Rate limit exceeded from JSON") as cm:
            client.get_completion("Test prompt")
        self.assertEqual(cm.exception.status_code, 429)
        self.assertEqual(cm.exception.details, error_json_payload)


    @patch('src.ai.xai_client.requests.post')
    @patch('src.ai.xai_client.get_config')
    def test_get_completion_connection_error(self, mock_get_config, mock_post):
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)
        mock_post.side_effect = requests.exceptions.ConnectionError("Failed to connect to host")
        
        client = XAIClient()
        with self.assertRaisesRegex(APIError, "API request failed due to a network/connection issue: Failed to connect to host"):
            client.get_completion("Test prompt")

    @patch('src.ai.xai_client.requests.post')
    @patch('src.ai.xai_client.get_config')
    def test_get_completion_uses_provided_tokens_temp(self, mock_get_config, mock_post):
        mock_get_config.side_effect = lambda key, default=None: self.mock_config_values.get(key, default)
        
        expected_response_json = {"choices": [{"text": "xAI response with custom params"}]}
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = expected_response_json
        mock_post.return_value = mock_response
        
        client = XAIClient()
        client.get_completion("Test", max_tokens=50, temperature=0.9, custom_param="test_val")
        
        mock_post.assert_called_once() # Ensure post was called
        _, kwargs = mock_post.call_args
        self.assertEqual(kwargs['json']['max_tokens'], 50)
        self.assertEqual(kwargs['json']['temperature'], 0.9)
        self.assertEqual(kwargs['json']['custom_param'], "test_val")

if __name__ == '__main__':
    unittest.main() 