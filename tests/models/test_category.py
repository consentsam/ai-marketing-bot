# Changelog:
# 2025-05-09 - Step 20 - Add tests for TweetCategory model.

import unittest
from src.models.category import TweetCategory

class TestTweetCategory(unittest.TestCase):
    def test_from_dict(self):
        data = {
            "name": "Announcement",
            "description": "Official announcement",
            "prompt_keywords": ["update", "news"],
            "style_guidelines": {"tone": "official"}
        }
        cat = TweetCategory.from_dict(data)
        self.assertEqual(cat.name, "Announcement")
        self.assertEqual(cat.description, "Official announcement")
        self.assertIn("update", cat.prompt_keywords)
        self.assertEqual(cat.style_guidelines["tone"], "official")

    def test_from_dict_missing_fields(self):
        data = {"name": "Test"}
        cat = TweetCategory.from_dict(data)
        self.assertEqual(cat.name, "Test")
        self.assertEqual(cat.description, "No description provided.")
        self.assertEqual(cat.prompt_keywords, [])
        self.assertEqual(cat.style_guidelines, {})

if __name__ == '__main__':
    unittest.main() 