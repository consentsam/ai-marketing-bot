import os
import json
import tempfile
import unittest
from datetime import datetime, timezone
from pathlib import Path

from src.utils.persistence import save_response
from src.models.response import AIResponse, ResponseType

class TestPersistence(unittest.TestCase):
    
    def setUp(self):
        # Create a temporary directory for test output
        self.temp_dir = tempfile.TemporaryDirectory()
        # Override the OUTPUT_DIR and GENERATED_FILE for testing
        from src.utils.persistence import OUTPUT_DIR, GENERATED_FILE
        self.original_output_dir = OUTPUT_DIR
        self.original_generated_file = GENERATED_FILE
        
        import src.utils.persistence as persistence
        persistence.OUTPUT_DIR = Path(self.temp_dir.name)
        persistence.GENERATED_FILE = Path(self.temp_dir.name) / 'test_replies_to_tweets.json'
    
    def tearDown(self):
        # Restore original paths
        import src.utils.persistence as persistence
        persistence.OUTPUT_DIR = self.original_output_dir
        persistence.GENERATED_FILE = self.original_generated_file
        # Clean up temp directory
        self.temp_dir.cleanup()
    
    def test_save_response_creates_new_file(self):
        """Test that save_response creates a new file if it doesn't exist."""
        # Create a test response
        response = AIResponse(
            content="Test tweet content",
            response_type=ResponseType.TWEET_REPLY,
            model_used="test-model",
            prompt_used="test prompt",
            generation_time=datetime.now(timezone.utc)
        )
        
        # Create test metadata
        metadata = {
            'original_input': 'Test input',
            'responding_as': 'TestAccount',
            'responding_as_type': 'Official'
        }
        
        # Call save_response
        save_response(response, metadata)
        
        # Check that file was created
        from src.utils.persistence import GENERATED_FILE
        self.assertTrue(GENERATED_FILE.exists())
        
        # Read file and verify content
        with open(GENERATED_FILE, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['response']['content'], "Test tweet content")
    
    def test_save_response_appends_to_existing_file(self):
        """Test that save_response appends to the file without overwriting."""
        from src.utils.persistence import GENERATED_FILE
        
        # Create an initial file with one entry
        initial_data = [{
            'saved_at': datetime.now(timezone.utc).isoformat(),
            'metadata': {'original_input': 'First tweet'},
            'response': {
                'content': 'First tweet content',
                'response_type': 'TWEET_REPLY',
                'model_used': 'test-model',
                'generation_time': datetime.now(timezone.utc).isoformat()
            }
        }]
        
        # Make sure the directory exists
        os.makedirs(os.path.dirname(GENERATED_FILE), exist_ok=True)
        
        # Write initial data
        with open(GENERATED_FILE, 'w') as f:
            json.dump(initial_data, f, indent=2)
        
        # Create a new response to append
        response = AIResponse(
            content="Second tweet content",
            response_type=ResponseType.TWEET_REPLY,
            model_used="test-model",
            prompt_used="test prompt",
            generation_time=datetime.now(timezone.utc)
        )
        
        # Create test metadata
        metadata = {
            'original_input': 'Second input',
            'responding_as': 'TestAccount',
            'responding_as_type': 'Official'
        }
        
        # Call save_response
        save_response(response, metadata)
        
        # Read file and verify content
        with open(GENERATED_FILE, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 2)
            self.assertEqual(data[0]['response']['content'], "First tweet content")
            self.assertEqual(data[1]['response']['content'], "Second tweet content")
    
    def test_save_response_handles_invalid_json(self):
        """Test that save_response handles invalid JSON in the existing file."""
        from src.utils.persistence import GENERATED_FILE
        
        # Create an initial file with invalid JSON
        os.makedirs(os.path.dirname(GENERATED_FILE), exist_ok=True)
        with open(GENERATED_FILE, 'w') as f:
            f.write("This is not valid JSON")
        
        # Create a new response
        response = AIResponse(
            content="New tweet content",
            response_type=ResponseType.TWEET_REPLY,
            model_used="test-model",
            prompt_used="test prompt",
            generation_time=datetime.now(timezone.utc)
        )
        
        # Create test metadata
        metadata = {
            'original_input': 'New input',
            'responding_as': 'TestAccount',
            'responding_as_type': 'Official'
        }
        
        # Call save_response
        save_response(response, metadata)
        
        # Read file and verify content
        with open(GENERATED_FILE, 'r') as f:
            data = json.load(f)
            self.assertIsInstance(data, list)
            self.assertEqual(len(data), 1)
            self.assertEqual(data[0]['response']['content'], "New tweet content") 