# Changelog:
# 2025-05-07 HH:MM - Step 20 (Initial) - Added comprehensive tests for config loading.
# 2025-05-07 HH:MM - Step 20 (Fix) - Patched DEFAULT_TEMPLATE in setUp for test isolation.
# 2025-05-07 HH:MM - Step 20 (Fix) - Adjusted tests for lowercase key normalization and fixed print assertion.

import unittest
from unittest.mock import patch, mock_open, call
import os
import yaml
import copy

# Ensure the test can find the src modules
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.config import settings as config_settings # type: ignore

# Store original _CONFIG_FILE_PATH and _ENV_FILE_PATH to restore later
_ORIGINAL_CONFIG_FILE_PATH = config_settings._CONFIG_FILE_PATH
_ORIGINAL_ENV_FILE_PATH = config_settings._ENV_FILE_PATH
_ORIGINAL_DEFAULT_TEMPLATE = copy.deepcopy(config_settings.DEFAULT_TEMPLATE)

# Define a base path for test artifacts
_TEST_ARTIFACTS_PATH = os.path.join(os.path.dirname(__file__), 'test_artifacts')
_MOCK_CONFIG_YAML_PATH = os.path.join(_TEST_ARTIFACTS_PATH, 'mock_config.yaml')
_MOCK_ENV_FILE_PATH = os.path.join(_TEST_ARTIFACTS_PATH, '.env.test')


class TestConfigSettings(unittest.TestCase):

    def setUp(self):
        """Set up for each test method."""
        os.makedirs(_TEST_ARTIFACTS_PATH, exist_ok=True)

        config_settings._CONFIG_FILE_PATH = _MOCK_CONFIG_YAML_PATH
        config_settings._ENV_FILE_PATH = _MOCK_ENV_FILE_PATH
        
        self.default_yaml_content = {
            'app_name': 'TestAppYAML',
            'log_level': 'DEBUG', # Lowercase key
            'ai': {
                'provider': 'yaml_provider', # Lowercase key
                'xai_api_key': 'yaml_xai_key',
                'default_temperature': 0.6
            },
            'data_sources': {
                'type': 'mock_yaml'
            }
        }
        with open(_MOCK_CONFIG_YAML_PATH, 'w') as f:
            yaml.dump(self.default_yaml_content, f)
            
        # No longer need to patch DEFAULT_TEMPLATE as load_config loads from file path
        # config_settings.DEFAULT_TEMPLATE = copy.deepcopy(self.default_yaml_content)

        self.default_env_content = """# .env keys are typically uppercase
        LOG_LEVEL=INFO_ENV
        AI__PROVIDER=env_provider
        AI__XAI_API_KEY=env_xai_key
        AI__GOOGLE_API_KEY=env_google_key
        NEW_SETTING=env_new_value
        """
        with open(_MOCK_ENV_FILE_PATH, 'w') as f:
            f.write(self.default_env_content)
            
        config_settings._CONFIG = {}
        config_settings._CONFIG_LOADED = False
            
        # Clear os.environ before each test to avoid interference
        current_keys = list(os.environ.keys())
        for key in current_keys:
            # Clear keys that might be loaded from .env or set directly
            if key in ['LOG_LEVEL', 'AI__PROVIDER', 'AI__XAI_API_KEY', 'AI__GOOGLE_API_KEY', 'NEW_SETTING', 'APP_NAME']:
                 if key in os.environ:
                    del os.environ[key]

    def tearDown(self):
        """Clean up after each test method."""
        config_settings._CONFIG_FILE_PATH = _ORIGINAL_CONFIG_FILE_PATH
        config_settings._ENV_FILE_PATH = _ORIGINAL_ENV_FILE_PATH
        # config_settings.DEFAULT_TEMPLATE = copy.deepcopy(_ORIGINAL_DEFAULT_TEMPLATE) # No longer needed

        if os.path.exists(_MOCK_CONFIG_YAML_PATH):
            os.remove(_MOCK_CONFIG_YAML_PATH)
        if os.path.exists(_MOCK_ENV_FILE_PATH):
            os.remove(_MOCK_ENV_FILE_PATH)
        if os.path.exists(_TEST_ARTIFACTS_PATH) and not os.listdir(_TEST_ARTIFACTS_PATH):
            os.rmdir(_TEST_ARTIFACTS_PATH)
        
        config_settings._CONFIG = {}
        config_settings._CONFIG_LOADED = False
        
        current_keys = list(os.environ.keys())
        for key in current_keys:
            if key in ['LOG_LEVEL', 'AI__PROVIDER', 'AI__XAI_API_KEY', 'AI__GOOGLE_API_KEY', 'NEW_SETTING', 'APP_NAME']:
                 if key in os.environ:
                    del os.environ[key]

    def test_load_config_from_yaml_and_env(self):
        """Test loading configuration from YAML and .env file, with .env overriding YAML via lowercase keys."""
        config = config_settings.load_config()

        self.assertEqual(config['app_name'], 'TestAppYAML') # From YAML, not in .env
        self.assertEqual(config['log_level'], 'INFO_ENV') # YAML 'log_level' overridden by .env 'LOG_LEVEL' (normalized)
        self.assertEqual(config['ai']['provider'], 'env_provider') # YAML 'provider' overridden by .env 'AI__PROVIDER' (normalized)
        self.assertEqual(config['ai']['xai_api_key'], 'env_xai_key') # Overridden by .env (normalized)
        self.assertEqual(config['ai']['google_api_key'], 'env_google_key') # New from .env (normalized)
        self.assertEqual(config['ai']['default_temperature'], 0.6) # From YAML
        self.assertEqual(config['data_sources']['type'], 'mock_yaml') # From YAML
        self.assertEqual(config['new_setting'], 'env_new_value') # New from .env (normalized)
        self.assertTrue(config_settings._CONFIG_LOADED)

    def test_get_config_loaded(self):
        """Test get_config when configuration is already loaded (case-insensitive)."""
        config_settings.load_config()
        self.assertEqual(config_settings.get_config('app_name'), 'TestAppYAML')
        self.assertEqual(config_settings.get_config('log_level'), 'INFO_ENV') # Check overridden value
        self.assertEqual(config_settings.get_config('AI.PROVIDER'), 'env_provider') # Case-insensitive get
        self.assertEqual(config_settings.get_config('ai.xai_api_key'), 'env_xai_key')
        self.assertEqual(config_settings.get_config('ai.default_temperature'), 0.6)
        self.assertEqual(config_settings.get_config('non_existent_key', 'default_val'), 'default_val')
        self.assertIsNone(config_settings.get_config('non_existent_key_no_default'))
        self.assertEqual(config_settings.get_config('AI.GOOGLE_API_KEY'), 'env_google_key') # Case-insensitive get

    def test_get_config_not_loaded_yet(self):
        """Test get_config calls load_config if not loaded yet."""
        self.assertFalse(config_settings._CONFIG_LOADED)
        self.assertEqual(config_settings.get_config('app_name'), 'TestAppYAML')
        self.assertTrue(config_settings._CONFIG_LOADED)
        self.assertEqual(config_settings.get_config('ai.provider'), 'env_provider') # Check overridden value
        self.assertEqual(config_settings.get_config('log_level'), 'INFO_ENV')

    def test_load_config_env_vars_override_everything(self):
        """Test that direct os.environ variables override YAML and .env file."""
        # Set os.environ AFTER .env would have been loaded by load_dotenv inside load_config
        os.environ['APP_NAME'] = 'OS_ENV_APP_NAME' # Should override YAML
        os.environ['LOG_LEVEL'] = 'OS_ENV_LOG_LEVEL' # Should override .env LOG_LEVEL
        # Note: The current direct os.environ override logic doesn't handle nested AI__PROVIDER well.
        # We rely on the .env loading via _update_dict_from_env for nested overrides.
        # Let's test overriding a nested value that *was* set by .env
        # Setting this BEFORE load_config means it should take precedence over the .env file value
        # because python-dotenv doesn't override existing env vars by default.
        os.environ['AI__XAI_API_KEY'] = 'OS_ENV_XAI_KEY' 

        config = config_settings.load_config()

        self.assertEqual(config['app_name'], 'OS_ENV_APP_NAME') # Direct os.environ override
        self.assertEqual(config['log_level'], 'OS_ENV_LOG_LEVEL') # Direct os.environ override
        # Check .env loaded values that weren't overridden by direct os.environ
        self.assertEqual(config['ai']['provider'], 'env_provider') # From .env
        self.assertEqual(config['ai']['google_api_key'], 'env_google_key') # From .env
        # Check the nested value - it should be the one from os.environ set before load_config
        self.assertEqual(config['ai']['xai_api_key'], 'OS_ENV_XAI_KEY') 

    @patch('builtins.print')
    def test_load_config_missing_yaml_file(self, mock_print):
        """Test behavior when config.yaml is missing."""
        if os.path.exists(_MOCK_CONFIG_YAML_PATH):
            os.remove(_MOCK_CONFIG_YAML_PATH)
        
        config = config_settings.load_config() # load_config will print warning
        
        # Check the specific warning message format
        expected_warning = f"Warning: Configuration file '{_MOCK_CONFIG_YAML_PATH}' not found. Using minimal defaults and environment variables."
        mock_print.assert_any_call(expected_warning)
        
        # Should load from .env only (normalized keys)
        self.assertEqual(config['log_level'], 'INFO_ENV') 
        self.assertEqual(config['ai']['provider'], 'env_provider')
        self.assertEqual(config['ai']['xai_api_key'], 'env_xai_key')
        self.assertNotIn('app_name', config) 
        self.assertIsNone(config_settings.get_config('app_name'))

    @patch('builtins.print')
    def test_load_config_malformed_yaml_file(self, mock_print):
        """Test behavior when config.yaml is malformed."""
        with open(_MOCK_CONFIG_YAML_PATH, 'w') as f:
            f.write("app_name: TestAppYAML\nlog_level: [Invalid YAML")
        
        config = config_settings.load_config()
        
        # Should load from .env only (normalized keys)
        self.assertEqual(config['log_level'], 'INFO_ENV')
        self.assertEqual(config['ai']['provider'], 'env_provider')
        # Check specific error message
        self.assertTrue(any("Unable to parse YAML" in call_args[0][0] for call_args in mock_print.call_args_list))
        self.assertNotIn('app_name', config)

    @patch('builtins.print')
    def test_load_config_empty_yaml_file(self, mock_print):
        """Test behavior when config.yaml is empty."""
        with open(_MOCK_CONFIG_YAML_PATH, 'w') as f:
            f.write("")
        
        config = config_settings.load_config()
                
        # Should load from .env only (normalized keys)
        self.assertEqual(config['log_level'], 'INFO_ENV') 
        self.assertEqual(config['ai']['provider'], 'env_provider') 
        self.assertNotIn('app_name', config)
        # Check warning for empty file
        mock_print.assert_any_call(f"Warning: Config file '{_MOCK_CONFIG_YAML_PATH}' is empty. Using minimal defaults.")

    def test_load_config_missing_env_file(self):
        """Test behavior when .env file is missing."""
        if os.path.exists(_MOCK_ENV_FILE_PATH):
            os.remove(_MOCK_ENV_FILE_PATH)
            
        config = config_settings.load_config()
        
        # Should load from YAML only (original keys)
        self.assertEqual(config['app_name'], 'TestAppYAML')
        self.assertEqual(config['log_level'], 'DEBUG') 
        self.assertEqual(config['ai']['provider'], 'yaml_provider')
        self.assertNotIn('google_api_key', config.get('ai', {}))

    def test_nested_key_retrieval_get_config(self):
        """Test get_config for deeply nested keys (case-insensitive)."""
        complex_yaml = {
            'level1': { # lowercase
                'LeVeL2': { # mixed case
                    'level3': 'value3',
                    'level3_alt': 'value3_alt'
                },
                'level2_alt': 'value2_alt'
            }
        }
        with open(_MOCK_CONFIG_YAML_PATH, 'w') as f:
            yaml.dump(complex_yaml, f)
        if os.path.exists(_MOCK_ENV_FILE_PATH):
            os.remove(_MOCK_ENV_FILE_PATH)
        
        config_settings._CONFIG = {} # Reset internal config
        config_settings._CONFIG_LOADED = False
        config_settings.load_config()
        
        self.assertEqual(config_settings.get_config('level1.level2.level3'), 'value3') # All lower
        self.assertEqual(config_settings.get_config('LEVEL1.LEVEL2.LEVEL3'), 'value3') # All upper
        self.assertEqual(config_settings.get_config('Level1.LeVeL2.Level3'), 'value3') # Mixed
        self.assertEqual(config_settings.get_config('level1.level2_alt'), 'value2_alt')
        self.assertIsNone(config_settings.get_config('level1.level2.non_existent'))
        self.assertEqual(config_settings.get_config('level1.non_existent.level3', 'default'), 'default')
        
    def test_get_config_returns_copy_not_original_dict(self):
        """Test that get_config returns a copy for dictionary values to prevent modification."""
        config_settings.load_config()
        ai_config_retrieved = config_settings.get_config('ai') # Should be lowercase 'ai' from normalized env
        self.assertIsNotNone(ai_config_retrieved) # Ensure 'ai' key exists
        # Assuming _CONFIG['ai'] exists and is a dict
        if 'ai' in config_settings._CONFIG and isinstance(config_settings._CONFIG['ai'], dict):
            original_ai_config_in_module = config_settings._CONFIG['ai']

            # Ensure it retrieves the correct dict (which includes .env overrides)
            self.assertEqual(ai_config_retrieved['provider'], 'env_provider')
            self.assertEqual(ai_config_retrieved['xai_api_key'], 'env_xai_key')
            
            # Modify the retrieved dict
            ai_config_retrieved['new_test_key'] = 'test_value'
            ai_config_retrieved['provider'] = 'modified_provider_in_retrieved'
            
            # Verify the original dict in the module is unchanged
            self.assertNotEqual(original_ai_config_in_module.get('provider'), 'modified_provider_in_retrieved')
            self.assertNotIn('new_test_key', original_ai_config_in_module)
            
            # Verify that a subsequent call to get_config returns the original, unmodified value
            ai_config_retrieved_again = config_settings.get_config('ai')
            self.assertEqual(ai_config_retrieved_again['provider'], 'env_provider') # Should be original
            self.assertNotIn('new_test_key', ai_config_retrieved_again)
        else:
            self.fail("config_settings._CONFIG['ai'] was not found or not a dict, prerequisite for this test failed.")

    def test_type_conversions_from_env(self):
        """Test correct type conversion for boolean, integer, and float from .env variables."""
        env_content_types = """
        MY_BOOL_TRUE=True
        MY_BOOL_FALSE=false
        MY_INT=123
        MY_FLOAT=45.67
        MY_STRING_INT=007
        MY_STRING_FLOAT=0.0
        MY_STRING=NotABoolOrNumber
        """
        with open(_MOCK_ENV_FILE_PATH, 'w') as f:
            f.write(env_content_types)
        
        # Clear YAML for this test to isolate .env effects
        with open(_MOCK_CONFIG_YAML_PATH, 'w') as f:
            yaml.dump({}, f)

        config_settings._CONFIG = {}
        config_settings._CONFIG_LOADED = False
        config = config_settings.load_config()

        self.assertIsInstance(config.get('my_bool_true'), bool)
        self.assertEqual(config.get('my_bool_true'), True)
        
        self.assertIsInstance(config.get('my_bool_false'), bool)
        self.assertEqual(config.get('my_bool_false'), False)
        
        self.assertIsInstance(config.get('my_int'), int)
        self.assertEqual(config.get('my_int'), 123)

        self.assertIsInstance(config.get('my_float'), float)
        self.assertEqual(config.get('my_float'), 45.67)

        self.assertIsInstance(config.get('my_string_int'), int) # "007" becomes int 7
        self.assertEqual(config.get('my_string_int'), 7)

        self.assertIsInstance(config.get('my_string_float'), float) # "0.0" becomes float 0.0
        self.assertEqual(config.get('my_string_float'), 0.0)

        self.assertIsInstance(config.get('my_string'), str)
        self.assertEqual(config.get('my_string'), 'NotABoolOrNumber')

    def test_set_config_value_simple(self):
        """Test setting a simple top-level config value."""
        config_settings.load_config() # Load initial config
        
        config_settings.set_config_value('new_runtime_setting', 'runtime_value')
        self.assertEqual(config_settings.get_config('new_runtime_setting'), 'runtime_value')
        
        config_settings.set_config_value('log_level', 'RUNTIME_DEBUG') # Override existing
        self.assertEqual(config_settings.get_config('log_level'), 'RUNTIME_DEBUG')

    def test_set_config_value_nested(self):
        """Test setting a nested config value, creating path if necessary."""
        config_settings.load_config()

        config_settings.set_config_value('new_parent.new_child.deep_setting', 'deep_value')
        self.assertEqual(config_settings.get_config('new_parent.new_child.deep_setting'), 'deep_value')
        
        # Check if parent dicts were created
        new_parent_config = config_settings.get_config('new_parent')
        self.assertIsInstance(new_parent_config, dict)
        self.assertIn('new_child', new_parent_config)
        self.assertIsInstance(new_parent_config['new_child'], dict)
        
        # Override existing nested value
        config_settings.set_config_value('ai.provider', 'runtime_ai_provider')
        self.assertEqual(config_settings.get_config('ai.provider'), 'runtime_ai_provider')

    def test_set_config_value_does_not_affect_loaded_copy(self):
        """Test that set_config_value modifies the internal _CONFIG, not copies from get_config."""
        config1 = config_settings.load_config()
        
        # Get a copy
        ai_config_copy = config_settings.get_config('ai')
        original_provider = ai_config_copy['provider'] # Should be 'env_provider'
        
        # Modify internal config via set_config_value
        config_settings.set_config_value('ai.provider', 'runtime_changed_provider')
        
        # The initial copy should be unchanged
        self.assertEqual(ai_config_copy['provider'], original_provider) 
        
        # A new call to get_config should reflect the change
        new_ai_config_copy = config_settings.get_config('ai')
        self.assertEqual(new_ai_config_copy['provider'], 'runtime_changed_provider')
        
        # The first fully loaded config object should also be unchanged if it was a deepcopy
        self.assertEqual(config1['ai']['provider'], original_provider)


if __name__ == '__main__':
    unittest.main() 