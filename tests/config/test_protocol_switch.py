"""
Tests for protocol switching functionality to verify Step 28: Alternate Protocol Example
"""

import os
import json
import unittest
from unittest.mock import patch
import tempfile
import shutil

from src.config.settings import get_config, set_config_value, get_protocol_path


class TestProtocolSwitch(unittest.TestCase):
    """Test cases for protocol switching functionality."""
    
    def setUp(self):
        # Store original protocol setting
        self.original_protocol = get_config("protocols.default_protocol", "ethena")
        
    def tearDown(self):
        # Restore original protocol setting
        set_config_value("protocols.default_protocol", self.original_protocol)
        
    def test_protocol_path_construction(self):
        """Test that protocol paths are correctly constructed for different protocols."""
        # Test ethena protocol path
        set_config_value("protocols.default_protocol", "ethena")
        ethena_path = get_protocol_path("categories.json")
        self.assertIn("protocols/ethena/categories.json", ethena_path)
        
        # Test exana protocol path
        set_config_value("protocols.default_protocol", "exana")
        exana_path = get_protocol_path("categories.json")
        self.assertIn("protocols/exana/categories.json", exana_path)
        
    def test_protocol_file_existence(self):
        """Test that expected files exist for both protocols."""
        # Check ethena files
        set_config_value("protocols.default_protocol", "ethena")
        ethena_files = [
            get_protocol_path("categories.json"),
            get_protocol_path("docs.md"),
            get_protocol_path("relevancy_facts.json"),
            get_protocol_path("mode-instructions", "InstructionsForDefault.md"),
            get_protocol_path("mode-instructions", "InstructionsForDegen.md"),
            get_protocol_path("mode-instructions", "InstructionsForProfessional.md")
        ]
        
        for file_path in ethena_files:
            self.assertTrue(os.path.exists(file_path), f"Ethena file missing: {file_path}")
            
        # Check exana files
        set_config_value("protocols.default_protocol", "exana")
        exana_files = [
            get_protocol_path("categories.json"),
            get_protocol_path("docs.md"),
            get_protocol_path("relevancy_facts.json"),
            get_protocol_path("mode-instructions", "InstructionsForDefault.md"),
            get_protocol_path("mode-instructions", "InstructionsForDegen.md"),
            get_protocol_path("mode-instructions", "InstructionsForProfessional.md")
        ]
        
        for file_path in exana_files:
            self.assertTrue(os.path.exists(file_path), f"Exana file missing: {file_path}")
    
    def test_protocol_content_differences(self):
        """Test that content differs between protocols for key files."""
        # Get ethena categories
        set_config_value("protocols.default_protocol", "ethena")
        ethena_categories_path = get_protocol_path("categories.json")
        with open(ethena_categories_path, 'r') as f:
            ethena_categories = json.load(f)
            
        # Get exana categories
        set_config_value("protocols.default_protocol", "exana")
        exana_categories_path = get_protocol_path("categories.json")
        with open(exana_categories_path, 'r') as f:
            exana_categories = json.load(f)
            
        # Verify categories are different
        ethena_category_names = [cat.get("name") for cat in ethena_categories.get("categories", [])]
        exana_category_names = [cat.get("name") for cat in exana_categories.get("categories", [])]
        
        self.assertNotEqual(ethena_category_names, exana_category_names, 
                           "Ethena and Exana should have different categories")
        
        # Also verify some content in the docs files is different
        set_config_value("protocols.default_protocol", "ethena")
        with open(get_protocol_path("docs.md"), 'r') as f:
            ethena_docs_content = f.read()
            
        set_config_value("protocols.default_protocol", "exana")
        with open(get_protocol_path("docs.md"), 'r') as f:
            exana_docs_content = f.read()
            
        self.assertNotEqual(ethena_docs_content, exana_docs_content,
                           "Protocol documentation content should differ")
        self.assertIn("Exana", exana_docs_content)
        
    def test_knowledge_source_with_protocol_switch(self):
        """Verify that changing the protocol affects knowledge source paths."""
        from src.knowledge.yieldfi import StaticJSONKnowledgeSource
        
        # Test with ethena protocol
        set_config_value("protocols.default_protocol", "ethena")
        ethena_source = StaticJSONKnowledgeSource()
        self.assertIn("ethena", ethena_source._file_path.lower())
        
        # Test with exana protocol
        set_config_value("protocols.default_protocol", "exana")
        exana_source = StaticJSONKnowledgeSource()
        self.assertIn("exana", exana_source._file_path.lower())


if __name__ == '__main__':
    unittest.main() 