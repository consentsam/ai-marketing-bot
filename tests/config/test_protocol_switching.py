"""
Simplified tests for protocol switching functionality to verify Step 28.
"""

import os
import json
import unittest
from unittest.mock import patch

from src.config.settings import get_protocol_path


class TestProtocolSwitchingSimple(unittest.TestCase):
    """Simplified test cases for protocol switching functionality."""
    
    def test_protocol_file_structures_exist(self):
        """Test that both protocols have the required file structures."""
        # Check that protocol directories exist
        ethena_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')), 
                                 "data", "protocols", "ethena")
        exana_dir = os.path.join(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')), 
                                "data", "protocols", "exana")
                                
        self.assertTrue(os.path.exists(ethena_dir), "Ethena protocol directory should exist")
        self.assertTrue(os.path.exists(exana_dir), "Exana protocol directory should exist")
        
        # Check required files in each protocol
        for protocol_dir in [ethena_dir, exana_dir]:
            self.assertTrue(os.path.exists(os.path.join(protocol_dir, "categories.json")))
            self.assertTrue(os.path.exists(os.path.join(protocol_dir, "docs.md")))
            self.assertTrue(os.path.exists(os.path.join(protocol_dir, "relevancy_facts.json")))
            self.assertTrue(os.path.exists(os.path.join(protocol_dir, "mode-instructions", "InstructionsForDefault.md")))
            self.assertTrue(os.path.exists(os.path.join(protocol_dir, "mode-instructions", "InstructionsForDegen.md")))
            self.assertTrue(os.path.exists(os.path.join(protocol_dir, "mode-instructions", "InstructionsForProfessional.md")))
    
    def test_protocol_content_differences(self):
        """Test that content differs between protocols for key files."""
        # Get base directory for protocol paths
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '../..'))
        
        # Load category files
        ethena_categories_path = os.path.join(base_dir, "data", "protocols", "ethena", "categories.json")
        exana_categories_path = os.path.join(base_dir, "data", "protocols", "exana", "categories.json")
        
        with open(ethena_categories_path, 'r') as f:
            ethena_categories = json.load(f)
            
        with open(exana_categories_path, 'r') as f:
            exana_categories = json.load(f)
            
        # Verify categories are different
        ethena_category_names = [cat.get("name") for cat in ethena_categories]
        exana_category_names = [cat.get("name") for cat in exana_categories]
        
        self.assertNotEqual(ethena_category_names, exana_category_names, 
                           "Ethena and Exana should have different categories")
        
        # Also verify some content in the docs files is different
        with open(os.path.join(base_dir, "data", "protocols", "ethena", "docs.md"), 'r') as f:
            ethena_docs_content = f.read()
            
        with open(os.path.join(base_dir, "data", "protocols", "exana", "docs.md"), 'r') as f:
            exana_docs_content = f.read()
            
        self.assertNotEqual(ethena_docs_content, exana_docs_content,
                           "Protocol documentation content should differ")
        self.assertIn("Exana", exana_docs_content)
        
    @patch('src.config.settings.get_config')
    def test_get_protocol_path_function(self, mock_get_config):
        """Test the get_protocol_path function."""
        # Test with ethena
        mock_get_config.return_value = "ethena"
        ethena_path = get_protocol_path("categories.json")
        self.assertIn("protocols/ethena/categories.json", ethena_path)
        
        # Test with exana
        mock_get_config.return_value = "exana"
        exana_path = get_protocol_path("categories.json")
        self.assertIn("protocols/exana/categories.json", exana_path)
        
        # Test with nested path
        mock_get_config.return_value = "exana"
        nested_path = get_protocol_path("mode-instructions", "InstructionsForDegen.md")
        self.assertIn("protocols/exana/mode-instructions/InstructionsForDegen.md", nested_path)


if __name__ == '__main__':
    unittest.main() 