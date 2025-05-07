# Changelog:
# 2025-05-08 00:00 - Step 20.0 - Initial creation and structure for model tests.
# 2025-05-08 00:00 - Step 20.1 - Fix field names in test_tweet_creation (removed view_count) and test_ai_response_creation (changed generation_time_ms to generation_time).

import pytest
from datetime import datetime
from src.models.account import Account, AccountType
from src.models.tweet import Tweet, TweetMetadata
from src.models.response import AIResponse, ResponseType
from src.models.category import TweetCategory # Assuming this is the path

# TODO: Add more comprehensive tests for each model, including:
# - from_dict and to_dict methods
# - Enum handling (e.g., AccountType.from_string)
# - Validation if any (e.g., required fields, type checks if not covered by dataclasses)
# - Edge cases (empty strings, None values where allowed/disallowed)

def test_account_creation():
    """Test basic Account model creation."""
    acc = Account(
        account_id="test_id_123",
        username="testuser",
        display_name="Test User",
        account_type=AccountType.OFFICIAL,
        platform="Twitter",
        follower_count=1000,
        bio="This is a test account.",
        interaction_history=[],
        tags=["test", "pytest"]
    )
    assert acc.username == "testuser"
    assert acc.account_type == AccountType.OFFICIAL

def test_tweet_creation():
    """Test basic Tweet model creation."""
    metadata = TweetMetadata(
        tweet_id="tweet123",
        created_at=datetime.now(),
        source="TestSource",
        author_id="author123",
        author_username="author_user",
        like_count=10,
        reply_count=2,
        retweet_count=5
    )
    tweet = Tweet(
        content="This is a test tweet!",
        metadata=metadata,
        tone="neutral",
        topics=["testing"],
        sentiment_score=0.0
    )
    assert tweet.content == "This is a test tweet!"
    assert tweet.metadata.tweet_id == "tweet123"

def test_ai_response_creation():
    """Test basic AIResponse model creation."""
    response = AIResponse(
        content="This is a generated reply.",
        response_type=ResponseType.TWEET_REPLY,
        model_used="test_model_v1",
        prompt_used="Test prompt",
        source_tweet_id="original_tweet_123",
        responding_as="YieldFiOfficial",
        target_account="TargetUser",
        tone="positive",
        generation_time=datetime.now()
    )
    assert response.response_type == ResponseType.TWEET_REPLY
    assert response.model_used == "test_model_v1"

def test_tweet_category_creation():
    """Test basic TweetCategory model creation."""
    category = TweetCategory(
        name="Product Update",
        description="Announcements about new product features or releases.",
        prompt_keywords=["new feature", "launch", "update"],
        style_guidelines={"tone": "informative", "length": "concise"}
    )
    assert category.name == "Product Update"
    assert "launch" in category.prompt_keywords

# Example for testing from_dict (needs actual implementation in models)
# def test_account_from_dict():
#     data = {
#         "account_id": "acc001",
#         "username": "dict_user",
#         "display_name": "User From Dict",
#         "account_type": "KOL", # Test string to Enum conversion
#         "platform": "Twitter",
#         "follower_count": 500,
#         "bio": "Bio here",
#         "interaction_history": [],
#         "tags": ["data"]
#     }
#     account = Account.from_dict(data)
#     assert account.username == "dict_user"
#     assert account.account_type == AccountType.KOL
#     assert account.follower_count == 500

# Example for testing to_dict (needs actual implementation in models)
# def test_tweet_to_dict():
#     metadata = TweetMetadata(tweet_id="twt002", created_at=datetime.now(), author_id="auth002", author_username="user2")
#     tweet = Tweet(content="Another tweet", metadata=metadata)
#     tweet_dict = tweet.to_dict()
#     assert tweet_dict["content"] == "Another tweet"
#     assert tweet_dict["metadata"]["tweet_id"] == "twt002" 