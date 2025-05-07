# Changelog:
# 2025-05-07 HH:MM - Step 5 (Testing) - Initial test structure for config settings.

import unittest
from unittest.mock import patch, mock_open
import os
import yaml

# Important: Need to import the module to be tested *after* potential patches, 
# or manage the global _config state carefully if testing multiple load scenarios.
# For simplicity here, we assume tests might influence each other if load_config is called multiple times.
# A better approach might involve resetting the _config global before each test or 
# structuring the config module differently (e.g., using a class).

import src.config.settings as config_settings

# Reset config before each test method to ensure isolation
def reset_config():
    config_settings._config = {}

class TestConfigSettings(unittest.TestCase):

    def setUp(self):
        """Reset the global config before each test."""
        reset_config()
        # Clear relevant environment variables before each test
        for key in ['DEBUG', 'LOG_LEVEL', 'DATA_SOURCE_TYPE', 'MY_ENV_VAR', 'NESTED_ENV_VAR']:
            if key in os.environ:
                del os.environ[key]

    def tearDown(self):
        """Ensure config is reset after tests if needed, though setUp handles it now."""
        reset_config()
        # Clean up env vars if necessary (handled in setUp mostly)
        for key in ['DEBUG', 'LOG_LEVEL', 'DATA_SOURCE_TYPE', 'MY_ENV_VAR', 'NESTED_ENV_VAR']:
            if key in os.environ:
                del os.environ[key]

    @patch("src.config.settings.load_dotenv") # Mock load_dotenv to avoid reading real .env
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_config_defaults_only(self, mock_file, mock_exists, mock_dotenv):
        """Test loading config when config.yaml and .env don't exist."""
        mock_exists.return_value = False # Simulate config.yaml not existing
        mock_dotenv.return_value = None # Simulate no .env loaded
        
        cfg = config_settings.load_config()
        
        self.assertEqual(cfg['app']['name'], 'YieldFi AI Agent')
        self.assertEqual(cfg['data_source']['type'], 'mock') # Default value
        self.assertFalse(cfg['app']['debug'])
        mock_dotenv.assert_called_once() # Ensure dotenv load was attempted
        mock_exists.assert_called_once_with('config.yaml') # Ensure yaml check happened

    @patch("src.config.settings.load_dotenv")
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_config_with_yaml(self, mock_file, mock_exists, mock_dotenv):
        """Test loading config with a mock config.yaml."""
        mock_exists.return_value = True
        mock_dotenv.return_value = None
        
        mock_yaml_content = yaml.dump({
            'app': {'name': 'YAML App Name'},
            'logging': {'level': 'DEBUG'}, # Overrides default
            'new_section': {'key': 'yaml_value'}
        })
        mock_file.return_value = mock_open(read_data=mock_yaml_content)()
        
        cfg = config_settings.load_config(config_file='mock_config.yaml')
        
        self.assertEqual(cfg['app']['name'], 'YAML App Name') # YAML override
        self.assertEqual(cfg['logging']['level'], 'DEBUG') # YAML override
        self.assertEqual(cfg['data_source']['type'], 'mock') # Default (not in YAML)
        self.assertEqual(cfg['new_section']['key'], 'yaml_value') # New section from YAML
        mock_exists.assert_called_once_with('mock_config.yaml')

    @patch("src.config.settings.load_dotenv")
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_config_empty_yaml(self, mock_file, mock_exists, mock_dotenv):
        """Test loading config when config.yaml is empty."""
        mock_exists.return_value = True
        mock_dotenv.return_value = None
        mock_file.return_value = mock_open(read_data="")() # Empty file

        cfg = config_settings.load_config(config_file='empty_config.yaml')
        
        # Expect defaults to be loaded
        self.assertEqual(cfg['app']['name'], 'YieldFi AI Agent')
        self.assertEqual(cfg['data_source']['type'], 'mock')
        mock_exists.assert_called_once_with('empty_config.yaml')

    @patch("src.config.settings.load_dotenv")
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    @patch("builtins.print") # Mock print to check for error messages
    def test_load_config_malformed_yaml(self, mock_print, mock_file, mock_exists, mock_dotenv):
        """Test loading config when config.yaml is malformed."""
        mock_exists.return_value = True
        mock_dotenv.return_value = None
        mock_file.return_value = mock_open(read_data="app: name: - Malformed YAML")() # Invalid YAML

        cfg = config_settings.load_config(config_file='malformed_config.yaml')
        
        # Expect defaults to be loaded
        self.assertEqual(cfg['app']['name'], 'YieldFi AI Agent')
        self.assertEqual(cfg['data_source']['type'], 'mock')
        mock_exists.assert_called_once_with('malformed_config.yaml')
        mock_print.assert_any_call(f"Error loading config file malformed_config.yaml: Unable to parse YAML.")

    @patch.dict(os.environ, {"LOG_LEVEL": "WARNING", "DATA_SOURCE_TYPE": "twitter", "MY_ENV_VAR": "env_value"})
    @patch("src.config.settings.load_dotenv")
    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def test_load_config_with_env_override(self, mock_file, mock_exists, mock_dotenv):
        """Test that environment variables override YAML and defaults."""
        mock_exists.return_value = True
        mock_dotenv.return_value = None # Assume .env doesn't add conflicting vars for this test
        
        mock_yaml_content = yaml.dump({
            'app': {'name': 'YAML App Name'},
            'logging': {'level': 'DEBUG'}, # Will be overridden by env var
            'data_source': {'type': 'yaml_source'} # Will be overridden by env var
        })
        mock_file.return_value = mock_open(read_data=mock_yaml_content)()

        # Also test direct os.environ.get in defaults
        os.environ['XAI_API_KEY'] = 'env_xai_key' 
        
        cfg = config_settings.load_config()
        
        # Env vars override YAML and defaults
        self.assertEqual(cfg['logging']['level'], 'WARNING') 
        self.assertEqual(cfg['data_source']['type'], 'twitter')
        self.assertEqual(cfg['ai']['xai_api_key'], 'env_xai_key') # From direct os.environ.get
        
        # Ensure default/YAML values are still there if not overridden
        self.assertEqual(cfg['app']['name'], 'YAML App Name')
        
        # Clean up env var used in default dict construction
        if 'XAI_API_KEY' in os.environ: del os.environ['XAI_API_KEY']

    def test_get_config_simple(self):
        """Test getting simple config values."""
        config_settings._config = {'app': {'name': 'Test App'}, 'logging': {'level': 'INFO'}}
        self.assertEqual(config_settings.get_config('app.name'), 'Test App')
        self.assertEqual(config_settings.get_config('logging.level'), 'INFO')
        
    def test_get_config_nested(self):
        """Test getting nested config values."""
        config_settings._config = {'data': {'source': {'twitter': {'api_key': '123'}}}}
        self.assertEqual(config_settings.get_config('data.source.twitter.api_key'), '123')

    def test_get_config_missing_key(self):
        """Test getting a missing key returns default."""
        config_settings._config = {'app': {'name': 'Test App'}}
        self.assertIsNone(config_settings.get_config('app.version'))
        self.assertEqual(config_settings.get_config('app.version', '1.0'), '1.0')
        self.assertEqual(config_settings.get_config('missing.nested.key', 'default_val'), 'default_val')

    def test_get_config_key_with_none_value(self):
        """Test getting a key that has a None value."""
        config_settings._config = {'app': {'version': None}}
        self.assertIsNone(config_settings.get_config('app.version'))
        self.assertIsNone(config_settings.get_config('app.version', 'default')) # Default should not be used if key exists

    def test_get_config_entire_dict(self):
        """Test getting the entire config dict."""
        test_dict = {'key1': 'val1', 'key2': {'nested': 'val2'}}
        config_settings._config = test_dict
        self.assertEqual(config_settings.get_config(), test_dict)

    def test_set_config_value_simple(self):
        """Test setting simple config values."""
        reset_config() # Start fresh
        config_settings._config = {'app': {'name': 'Original'}}
        config_settings.set_config_value('app.name', 'Updated')
        self.assertEqual(config_settings.get_config('app.name'), 'Updated')
        config_settings.set_config_value('new_key', 'new_value')
        self.assertEqual(config_settings.get_config('new_key'), 'new_value')

    def test_set_config_value_nested(self):
        """Test setting nested config values."""
        reset_config()
        config_settings._config = {'data': {'source': {'type': 'mock'}}}
        config_settings.set_config_value('data.source.api_key', 'xyz')
        self.assertEqual(config_settings.get_config('data.source.api_key'), 'xyz')
        self.assertEqual(config_settings.get_config('data.source.type'), 'mock') # Ensure original nested keys remain

        # Test creating intermediate dictionaries
        config_settings.set_config_value('new.nested.structure', 'deep_value')
        self.assertEqual(config_settings.get_config('new.nested.structure'), 'deep_value')
        self.assertIsInstance(config_settings.get_config('new'), dict)
        self.assertIsInstance(config_settings.get_config('new.nested'), dict)

        # Test creating multiple levels of non-existent nested structures
        config_settings.set_config_value('very.deep.nested.structure.level', 'ultra_deep_value')
        self.assertEqual(config_settings.get_config('very.deep.nested.structure.level'), 'ultra_deep_value')
        self.assertIsInstance(config_settings.get_config('very'), dict)
        self.assertIsInstance(config_settings.get_config('very.deep'), dict)
        self.assertIsInstance(config_settings.get_config('very.deep.nested'), dict)
        self.assertIsInstance(config_settings.get_config('very.deep.nested.structure'), dict)

if __name__ == '__main__':
    unittest.main() 