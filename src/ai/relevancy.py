import json
import os
from typing import List, Optional

from src.models.tweet import Tweet  # type: ignore
from src.config import get_protocol_path  # Step 27 - Protocol paths

# Changelog:
# 2025-05-19 14:30 - Step 26 - Initial implementation of relevancy facts.
# 2025-05-19 15:00 - Step 27 - Updated to use protocol paths.

def get_facts(tweet: Tweet) -> List[str]:
    """
    Retrieve relevancy facts based on keywords found in the tweet content.

    Args:
        tweet: Tweet object to analyze.

    Returns:
        A list of relevant fact strings matching conditions in the tweet content.
    """
    facts: List[str] = []
    content_lower = tweet.content.lower()

    # Get path to relevancy facts file using protocol paths (Step 27)
    facts_file_path = get_protocol_path('relevancy_facts.json')

    try:
        with open(facts_file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        # No relevancy facts file found
        return []
    except json.JSONDecodeError:
        # Invalid JSON format
        return []

    # Data can be a dict mapping conditions to facts
    if isinstance(data, dict):
        for condition, fact in data.items():
            if condition.lower() in content_lower:
                facts.append(fact)
    # Data can be a list of dicts with condition/fact keys
    elif isinstance(data, list):
        for entry in data:
            condition = entry.get('condition', '').lower()
            fact = entry.get('fact')
            if condition and fact and condition in content_lower:
                facts.append(fact)

    return facts 