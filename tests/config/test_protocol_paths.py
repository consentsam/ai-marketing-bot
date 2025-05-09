import os
import unittest
from unittest.mock import patch, MagicMock

from src.config import get_protocol_path, get_config

class TestProtocolPaths(unittest.TestCase):
    
    def setUp(self):
        # Ensure we have a base protocol directory for testing
        os.makedirs("data/protocols/test_protocol", exist_ok=True)
        # Create a test file
        with open("data/protocols/test_protocol/test_file.txt", "w") as f:
            f.write("Test content")
    
    def tearDown(self):
        # Clean up test files
        if os.path.exists("data/protocols/test_protocol/test_file.txt"):
            os.remove("data/protocols/test_protocol/test_file.txt")
    
    @patch('src.config.settings.get_config')
    def test_get_protocol_path_default(self, mock_get_config):
        # Test with default protocol (ethena)
        mock_get_config.return_value = "ethena"
        path = get_protocol_path("test_file.txt")
        self.assertIn("data/protocols/ethena/test_file.txt", path)
    
    @patch('src.config.settings.get_config')
    def test_get_protocol_path_custom(self, mock_get_config):
        # Test with custom protocol
        mock_get_config.return_value = "test_protocol"
        path = get_protocol_path("test_file.txt")
        self.assertIn("data/protocols/test_protocol/test_file.txt", path)
        # Verify the file exists
        self.assertTrue(os.path.exists(path))
    
    @patch('src.config.settings.get_config')
    def test_get_protocol_path_with_multiple_parts(self, mock_get_config):
        # Test with nested paths
        mock_get_config.return_value = "ethena"
        path = get_protocol_path("mode-instructions", "InstructionsForDefault.md")
        self.assertIn("data/protocols/ethena/mode-instructions/InstructionsForDefault.md", path)
    
    @patch('src.config.settings.get_config')
    def test_get_protocol_path_nonexistent_protocol(self, mock_get_config):
        # Test with nonexistent protocol
        mock_get_config.return_value = "nonexistent_protocol"
        # This should not raise an error, just return the path
        path = get_protocol_path("test_file.txt")
        self.assertIn("data/protocols/nonexistent_protocol/test_file.txt", path)
        # But the path should not exist
        self.assertFalse(os.path.exists(path))

if __name__ == '__main__':
    unittest.main() 