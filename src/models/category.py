# Changelog:
# 2025-05-07 HH:MM - Step 17 - Initial creation of TweetCategory model.

from dataclasses import dataclass, field
from typing import List, Dict, Any

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

if __name__ == '__main__':
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