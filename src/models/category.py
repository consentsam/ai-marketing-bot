# Changelog:
# 2025-05-07 HH:MM - Step 17 - Initial creation with TweetCategory dataclass and load_categories function.
# 2025-05-19 15:00 - Step 27 - Updated to use protocol paths.

"""
Models for tweet categories.

Purpose: Defines the data structure for tweet categories and provides
         functionality to load them from a JSON file.
Rationale: A structured way to define and load categories is essential
           for managing them and for the AI to generate targeted content.
Usage: Import TweetCategory and use load_categories() to get a list of available
       tweet categories.
"""

import json
import os
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from src.config import get_config, get_protocol_path  # Step 27 - Protocol paths

@dataclass
class TweetCategory:
    """
    Represents a category for generating new tweets, including guidance for the AI.
    """
    name: str
    description: str
    prompt_keywords: List[str] = field(default_factory=list)
    style_guidelines: Dict[str, str] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'TweetCategory':
        """Creates a TweetCategory instance from a dictionary."""
        return cls(
            name=data.get("name", "Unnamed Category"),
            description=data.get("description", "No description provided."),
            prompt_keywords=data.get("prompt_keywords", []),
            style_guidelines=data.get("style_guidelines", {})
        )

    def __str__(self) -> str:
        return self.name

def load_categories(categories_file_path: Optional[str] = None) -> List[TweetCategory]:
    """
    Loads tweet categories from a JSON file.

    Args:
        categories_file_path: Optional path to the categories JSON file.
                              If None, the protocol-specific path is used.

    Returns:
        A list of TweetCategory objects.
        Returns an empty list if the file is not found or is invalid.
    """
    if categories_file_path is None:
        # Use protocol paths from Step 27
        categories_file_path = get_protocol_path("categories.json")

    if not os.path.exists(categories_file_path):
        protocol = get_config("default_protocol", "ethena")
        print(f"Error: Categories file not found at {categories_file_path} for protocol '{protocol}'")
        return []
    
    try:
        with open(categories_file_path, 'r') as f:
            data = json.load(f)
        
        if not isinstance(data, list):
            print(f"Error: Categories file {categories_file_path} does not contain a list.")
            return []
            
        categories = [TweetCategory.from_dict(item) for item in data if isinstance(item, dict)]
        return categories
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {categories_file_path}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred while loading categories: {e}")
        return []

if __name__ == '__main__':
    # This is for basic testing of this module
    # To run this, ensure your project root is in PYTHONPATH
    # and you have a valid data/input/categories.json
    # Example: python -m src.models.category
    
    # Assuming project root is added to PYTHONPATH
    # and config.yaml is accessible for get_config to function correctly.
    # For standalone test, might need to mock get_config or provide path directly.
    
    print("Testing category loading...")
    # Test with default path resolution via get_config
    # For this to work, load_config() in settings must be callable and config.yaml present
    # If running from project root: python -m src.models.category
    # Ensure .env and config.yaml are present for settings.py to load correctly.
    
    # Fallback path for direct script execution if get_config fails or not setup
    # This assumes your CWD is the project root when running `python src/models/category.py`
    # A more robust test would mock get_config or use a test-specific config file.
    
    # Attempt to load config for get_config to work
    try:
        from src.config.settings import load_config
        load_config() # Initialize configuration
    except Exception as e:
        print(f"Could not load main config for testing: {e}")


    categories = load_categories()
    if categories:
        print(f"Loaded {len(categories)} categories:")
        for category in categories:
            print(f"- Name: {category.name}")
            print(f"  Description: {category.description[:60]}...")
            print(f"  Keywords: {category.prompt_keywords}")
            print(f"  Style Tone: {category.style_guidelines.get('tone')}")
    else:
        print("No categories loaded. Check file path and JSON format.")

    # Test with explicit path (if you want to bypass config for a quick check)
    # test_file_path = os.path.join(os.path.dirname(__file__), '..', '..', 'data', 'input', 'categories.json')
    # print(f"\nTesting with explicit path: {test_file_path}")
    # categories_explicit = load_categories(categories_file_path=test_file_path)
    # if categories_explicit:
    #     print(f"Loaded {len(categories_explicit)} categories explicitly.")
    # else:
    #     print("No categories loaded with explicit path.")


    # Example usage
    sample_data = {
        "name": "Product Update",
        "description": "Announce new features, improvements, or releases related to YieldFi products.",
        "prompt_keywords": ["new feature", "product launch", "update available", "enhancement"],
        "style_guidelines": {
            "tone": "Informative and exciting",
            "length": "Concise, ideally under 200 characters",
            "call_to_action": "Encourage users to try the new feature or learn more"
        }
    }
    category_from_dict = TweetCategory.from_dict(sample_data)
    print(f"Category from dict: {category_from_dict.name}, Description: {category_from_dict.description}")
    print(f"Keywords: {category_from_dict.prompt_keywords}")
    print(f"Style: {category_from_dict.style_guidelines}")

    direct_category = TweetCategory(
        name="Community Engagement",
        description="Share community news, highlight user contributions, or ask engaging questions.",
        prompt_keywords=["community spotlight", "AMA", "user feedback", "join the conversation"],
        style_guidelines={"tone": "Friendly and inclusive"}
    )
    print(f"Directly created category: {direct_category}") 