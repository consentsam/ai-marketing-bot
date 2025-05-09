# Changelog:
# 2025-05-09 - Step 20 - Add tests for image generation module.

import unittest
import os
from unittest.mock import patch, MagicMock

from src.ai.image_generation import get_poster_image

class TestImageGeneration(unittest.TestCase):
    @patch.dict(os.environ, {"GROK_IMAGE_API_KEY": "dummy_key"})
    @patch('src.ai.image_generation.requests.post')
    def test_get_poster_image_success(self, mock_post):
        # Mock a successful API response
        mock_resp = MagicMock()
        mock_resp.raise_for_status.return_value = None
        mock_resp.json.return_value = {"data": [{"url": "http://fake.url/image.jpg"}]}
        mock_post.return_value = mock_resp
        url = get_poster_image("Test prompt for poster image.")
        self.assertEqual(url, "http://fake.url/image.jpg")

    @patch.dict(os.environ, {}, clear=True)
    @patch('src.ai.image_generation.get_config')
    def test_get_poster_image_no_api_key(self, mock_get_config):
        mock_get_config.return_value = None
        # No API key in environment, should return placeholder for missing key
        url = get_poster_image("Another test prompt.")
        self.assertTrue(url.startswith("https://placehold.co/512x512?text=No+API+Key"))

    @patch.dict(os.environ, {"GROK_IMAGE_API_KEY": "dummy_key"})
    @patch('src.ai.image_generation.requests.post')
    def test_get_poster_image_api_error(self, mock_post):
        # Simulate an exception during the API call
        mock_post.side_effect = Exception("API down")
        url = get_poster_image("Another test prompt.")
        self.assertTrue(url.startswith("https://placehold.co/512x512?text=Image+Error"))

if __name__ == '__main__':
    unittest.main() 