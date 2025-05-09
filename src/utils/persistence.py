"""
Persistence utilities for saving generated AI responses.
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional

from src.config.settings import get_config
from src.models.response import AIResponse
import logging

logger = logging.getLogger(__name__)

# Determine output directory and file name from config
OUTPUT_DIR = Path(get_config('data_paths.output', 'data/output'))
# Use a fixed file name; could make configurable
GENERATED_FILE = OUTPUT_DIR / 'generated_tweets.json'


def save_response(
    response: AIResponse,
    metadata: Dict[str, Any]
) -> None:
    """
    Save an AIResponse along with metadata to the generated_tweets.json file.

    Args:
        response: The AIResponse object to save.
        metadata: A dict of metadata about the generation (e.g., original input, mode, responding_as, target_account).
    """
    try:
        # Ensure output directory exists
        OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        
        # Prepare the new entry
        entry: Dict[str, Any] = {
            'saved_at': response.generation_time.isoformat(),
            'metadata': metadata,
            'response': response.to_dict()
        }
        
        # If file doesn't exist, create a new list
        if not GENERATED_FILE.exists():
            logger.info(f"Creating new file: {GENERATED_FILE}")
            with open(GENERATED_FILE, 'w') as f:
                json.dump([entry], f, indent=2)
            logger.info(f"Created generated tweets file and saved entry: {GENERATED_FILE}")
            return
            
        # Load existing data
        try:
            with open(GENERATED_FILE, 'r') as f:
                try:
                    data = json.load(f)
                    # Verify it's a list
                    if not isinstance(data, list):
                        logger.warning(f"File {GENERATED_FILE} doesn't contain a valid list, resetting to empty list")
                        data = []
                except json.JSONDecodeError as e:
                    logger.warning(f"Could not decode JSON from {GENERATED_FILE}: {e}. Resetting to empty list.")
                    data = []
        except Exception as e:
            logger.error(f"Error reading {GENERATED_FILE}: {e}")
            data = []
                
        # Append new entry
        data.append(entry)
        
        # Write back to file - use a temporary file to prevent corruption if process is interrupted
        import tempfile
        import os
        import shutil
        
        temp_fd, temp_path = tempfile.mkstemp(prefix='tweets_', suffix='.json', dir=OUTPUT_DIR)
        try:
            # Write to temp file first
            with os.fdopen(temp_fd, 'w') as temp_file:
                json.dump(data, temp_file, indent=2)
            
            # Replace original file with temp file
            shutil.move(temp_path, GENERATED_FILE)
            logger.info(f"Successfully saved response to {GENERATED_FILE} (now contains {len(data)} entries)")
        except Exception as e:
            logger.error(f"Error writing to temporary file {temp_path}: {e}")
            # Try to clean up temp file if it still exists
            if os.path.exists(temp_path):
                os.unlink(temp_path)
            raise
            
    except Exception as e:
        logger.error(f"Failed to save response to {GENERATED_FILE}: {e}", exc_info=True) 