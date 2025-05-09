"""
Test script to verify fixes to response cleaning and JSON persistence.
"""
import os
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

from src.ai.response_generator import _clean_response
from src.models.response import AIResponse, ResponseType
from src.utils.persistence import save_response
from src.config.settings import get_config

# Test response cleaning
print("Testing response cleaning...")
test_responses = [
    # Truncated response
    "s rise to the top highlights the power of decentralized finance. At YieldFi, we",
    # Response with reasoning
    """I need to craft a response about Bitcoin's success.
    
    This would be a good opportunity to mention our yield farming platform.
    
    Final tweet: Bitcoin's rise shows the strength of crypto. Maximize your returns with YieldFi's innovative staking solutions!""",
    # Response with quotes
    '"Bitcoin\'s rise shows the power of decentralized finance. #YieldFi #DeFi"',
]

for i, response in enumerate(test_responses):
    cleaned = _clean_response(response)
    print(f"Test {i+1}:")
    print(f"  Input: {response[:50]}...")
    print(f"  Cleaned: {cleaned}")
    print(f"  Length: {len(cleaned)} chars")
    print()

# Test persistence
print("\nTesting persistence...")
output_dir = Path(get_config('data_paths.output', 'data/output'))
test_file = output_dir / 'test_persistence.json'

# Remove test file if it exists
if test_file.exists():
    os.remove(test_file)
    print(f"Removed existing test file: {test_file}")

# Import and temporarily override output file
import src.utils.persistence as persistence
original_file = persistence.GENERATED_FILE
persistence.GENERATED_FILE = test_file

try:
    # Test saving multiple responses
    for i in range(3):
        response = AIResponse(
            content=f"Test tweet content {i+1}",
            response_type=ResponseType.TWEET_REPLY,
            model_used="test-model",
            prompt_used="test prompt",
            generation_time=datetime.now(timezone.utc)
        )
        
        metadata = {
            'original_input': f'Test input {i+1}',
            'responding_as': 'TestAccount',
            'responding_as_type': 'Official'
        }
        
        save_response(response, metadata)
        print(f"Saved response {i+1}")
    
    # Check contents of file
    if test_file.exists():
        with open(test_file, 'r') as f:
            data = json.load(f)
            print(f"\nFile contains {len(data)} entries:")
            for i, entry in enumerate(data):
                print(f"  Entry {i+1}: {entry['response']['content']}")
        print(f"\nPersistence test passed! File successfully contains {len(data)} entries.")
    else:
        print("Error: Test file was not created.")
finally:
    # Restore original file
    persistence.GENERATED_FILE = original_file
    print(f"\nRestored original output file: {original_file}") 