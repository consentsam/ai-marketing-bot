"""
Tests for verifying the Vercel deployment configuration.

This tests that our Vercel deployment configuration is valid and should work properly
when deployed to Vercel.
"""

import json
import os
import subprocess
import sys
import pytest

# Basic test to validate vercel.json syntax
def test_vercel_json_valid():
    """Test that vercel.json is a valid JSON file with the expected structure."""
    try:
        with open('vercel.json', 'r') as f:
            vercel_config = json.load(f)
        
        # Assert that required keys are present
        assert 'builds' in vercel_config, "Missing 'builds' key in vercel.json"
        assert 'routes' in vercel_config, "Missing 'routes' key in vercel.json"
        
        # Check specific configuration for builds (using the Python builder)
        assert len(vercel_config['builds']) > 0, "No build configurations defined"
        assert vercel_config['builds'][0]['use'] == "@vercel/python", "Not using @vercel/python builder"
        assert 'src' in vercel_config['builds'][0], "No source file specified for build"
        
        # Check routes configuration
        assert len(vercel_config['routes']) > 0, "No routes defined"
        assert 'src' in vercel_config['routes'][0], "No source pattern for route"
        assert 'dest' in vercel_config['routes'][0], "No destination for route"
        
    except FileNotFoundError:
        pytest.fail("vercel.json file not found")
    except json.JSONDecodeError:
        pytest.fail("vercel.json is not valid JSON")

# Test that runtime.txt contains a valid Python version
def test_runtime_txt_valid():
    """Test that runtime.txt contains a valid Python version string."""
    try:
        with open('runtime.txt', 'r') as f:
            runtime = f.read().strip()
        
        assert runtime.startswith('python-'), "runtime.txt must start with 'python-'"
        
        # Extract version and validate format (should be python-X.Y.Z)
        version = runtime.replace('python-', '')
        version_parts = version.split('.')
        assert len(version_parts) >= 2, "Invalid Python version format (should be X.Y.Z)"
        
        # Basic validation that major and minor versions are integers
        assert version_parts[0].isdigit(), "Major version must be a number"
        assert version_parts[1].isdigit(), "Minor version must be a number"
        
    except FileNotFoundError:
        pytest.fail("runtime.txt file not found")

# Test that start.sh is executable and has the right permissions
def test_start_sh_executable():
    """Test that scripts/start.sh is executable."""
    start_sh_path = 'scripts/start.sh'
    
    try:
        # Check if file exists
        assert os.path.isfile(start_sh_path), "scripts/start.sh file not found"
        
        # Check if file is executable (on Unix systems)
        if sys.platform != 'win32':
            assert os.access(start_sh_path, os.X_OK), "scripts/start.sh is not executable"
            
        # On Windows, just check that it exists as we can't check execute permissions
    except Exception as e:
        pytest.fail(f"Error checking start.sh: {str(e)}")

# Test that start.sh handles the PORT environment variable correctly
def test_start_sh_port_handling():
    """Test that scripts/start.sh correctly handles the PORT environment variable."""
    start_sh_path = 'scripts/start.sh'
    
    try:
        # Read the start.sh file
        with open(start_sh_path, 'r') as f:
            content = f.read()
        
        # Check if it references PORT variable
        assert 'PORT' in content, "scripts/start.sh does not reference PORT environment variable"
        
        # Check if it sets a default PORT if not provided
        assert 'if [ -z "$PORT" ]' in content, "scripts/start.sh does not check if PORT is empty"
        assert 'export PORT=' in content, "scripts/start.sh does not set a default PORT"
        
        # Check if it uses PORT with streamlit run
        assert 'streamlit run' in content, "scripts/start.sh does not run streamlit"
        assert '--server.port "$PORT"' in content, "scripts/start.sh does not set server.port to $PORT"
        
    except FileNotFoundError:
        pytest.fail("scripts/start.sh file not found")
    except Exception as e:
        pytest.fail(f"Error checking start.sh PORT handling: {str(e)}") 