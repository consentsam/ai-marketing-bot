"""
Tests for verifying the documentation files.

This module checks that documentation files exist and contain the expected content (like mentions of image generation and Vercel deployment)
"""

import os
import unittest

class TestDocumentation(unittest.TestCase):
    """Test the documentation files for completeness."""
    
    def test_readme_exists(self):
        """Test that the README.md file exists."""
        self.assertTrue(os.path.exists('README.md'), "README.md file not found")
    
    def test_readme_contains_essential_info(self):
        """Test that README.md contains essential information about features."""
        with open('README.md', 'r') as f:
            readme_content = f.read()
        
        # Check for feature descriptions
        self.assertIn('Image Generation', readme_content, "README.md should mention Image Generation feature")
        self.assertIn('GROK_IMAGE_API_KEY', readme_content, "README.md should mention GROK_IMAGE_API_KEY")
        self.assertIn('DEFAULT_PROTOCOL', readme_content, "README.md should mention DEFAULT_PROTOCOL environment variable")
        self.assertIn('Vercel', readme_content, "README.md should mention Vercel deployment")
    
    def test_usage_doc_exists(self):
        """Test that the usage.md file exists."""
        self.assertTrue(os.path.exists('docs/usage.md'), "docs/usage.md file not found")
    
    def test_usage_doc_contains_essential_info(self):
        """Test that usage.md contains essential information about features."""
        with open('docs/usage.md', 'r') as f:
            usage_content = f.read()
        
        # Check for feature usage instructions
        self.assertIn('Generate Poster Image', usage_content, "usage.md should mention 'Generate Poster Image' checkbox")
        self.assertIn('Category Selection', usage_content, "usage.md should mention Category Selection")
        self.assertIn('Image Generation', usage_content, "usage.md should mention Image Generation feature")
    
    def test_api_doc_exists(self):
        """Test that the api.md file exists."""
        self.assertTrue(os.path.exists('docs/api.md'), "docs/api.md file not found")
    
    def test_api_doc_contains_essential_info(self):
        """Test that api.md contains essential API documentation."""
        with open('docs/api.md', 'r') as f:
            api_content = f.read()
        
        # Check for API documentation
        self.assertIn('image_url', api_content, "api.md should document the 'image_url' field in AIResponse")
        self.assertIn('generate_image', api_content, "api.md should document the 'generate_image' parameter")
        self.assertIn('src/ai/image_generation.py', api_content, "api.md should mention the image_generation module")
    
    def test_deployment_doc_exists(self):
        """Test that the deployment.md file exists."""
        self.assertTrue(os.path.exists('docs/deployment.md'), "docs/deployment.md file not found")
    
    def test_deployment_doc_contains_essential_info(self):
        """Test that deployment.md contains essential deployment information."""
        with open('docs/deployment.md', 'r') as f:
            deployment_content = f.read()
        
        # Check for deployment documentation
        self.assertIn('Vercel', deployment_content, "deployment.md should document Vercel deployment")
        self.assertIn('XAI_API_KEY', deployment_content, "deployment.md should mention necessary environment variables")
        self.assertIn('GROK_IMAGE_API_KEY', deployment_content, "deployment.md should mention GROK_IMAGE_API_KEY")
        self.assertIn('vercel.json', deployment_content, "deployment.md should mention vercel.json configuration")
        self.assertIn('runtime.txt', deployment_content, "deployment.md should mention runtime.txt")

if __name__ == '__main__':
    unittest.main() 