# Changelog:
# 2025-05-08 00:00 - Step 20.0 - Initial creation and structure for model tests.
# 2025-05-08 00:00 - Step 20.1 - Fix field names in test_tweet_creation (removed view_count) and test_ai_response_creation (changed generation_time_ms to generation_time).
# 2025-05-17 10:00 - Step 20.2 - Added comprehensive tests for from_dict, to_dict, enum handling, datetime handling, and validations for all models.

import pytest
from datetime import datetime, timezone
import copy # For deepcopy
from unittest.mock import patch # Added for patching in test_load_categories_function_from_category_module

# Ensure the test can find the src modules
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from src.models.account import Account, AccountType
from src.models.tweet import Tweet, TweetMetadata
from src.models.response import AIResponse, ResponseType
from src.models.category import TweetCategory

# --- Test Data ---
NOW = datetime.now(timezone.utc) # Use timezone-aware datetime
NOW_ISO = NOW.isoformat()

RAW_ACCOUNT_DATA = {
    "account_id": "acc001",
    "username": "dict_user",
    "display_name": "User From Dict",
    "account_type": "KOL", # Test string to Enum conversion
    "platform": "TestPlatform",
    "follower_count": 500,
    "following_count": 50,
    "verified": True,
    "is_following_yieldfi": True,
    "followed_by_yieldfi": False,
    "interaction_history": [{"type": "reply", "tweet_id": "twt000"}],
    "bio": "Bio here for dict_user",
    "location": "TestLocation",
    "website": "https://example.com/dict_user",
    "created_at": NOW_ISO, # Use ISO string for testing
    "tags": ["data", "kol_tag"],
    "notes": "Some notes for dict_user"
}

RAW_TWEET_METADATA_DATA = {
    "tweet_id": "meta_twt001",
    "created_at": NOW_ISO,
    "source": "TestAPI",
    "author_id": "meta_auth001",
    "author_username": "meta_user",
    "author_name": "Meta Author",
    "author_verified": True,
    "author_follower_count": 1200,
    "like_count": 150,
    "retweet_count": 30,
    "reply_count": 10,
    "quote_count": 5,
    "in_reply_to_tweet_id": "meta_orig_twt002",
    "in_reply_to_user_id": "meta_orig_user002",
    "mentioned_users": ["@mentioned1", "@mentioned2"],
    "hashtags": ["#test", "#metadata"],
    "urls": ["https://example.com/meta_link"],
    "extra_data": {"lang": "en", "custom_field": "meta_value"}
}

# Note: Tweet.from_dict requires \'id\' and \'content\' at the top level,
# and other fields are nested or direct.
RAW_TWEET_DATA = {
    "id": "twt002", # Corresponds to metadata.tweet_id
    "content": "Another tweet from dict",
    "created_at": NOW_ISO, # Corresponds to metadata.created_at
    "source": "APISource", # metadata.source
    "author_id": "auth002", # metadata.author_id
    "author_username": "user2_dict", # metadata.author_username
    "author_name": "User Two Dict", # metadata.author_name
    "author_verified": False, # metadata.author_verified
    "author_follower_count": 750, # metadata.author_follower_count
    "like_count": 25, # metadata.like_count
    "retweet_count": 3, # metadata.retweet_count
    "reply_count": 1, # metadata.reply_count
    "quote_count": 0, # metadata.quote_count
    "in_reply_to_tweet_id": "orig_twt003", # metadata.in_reply_to_tweet_id
    "in_reply_to_user_id": "orig_user003", # metadata.in_reply_to_user_id
    "mentioned_users": ["@mention_dict"], # metadata.mentioned_users
    "hashtags": ["#dictTweet"], # metadata.hashtags
    "urls": ["https://example.com/dict_url"], # metadata.urls
    "extra_data": {"source_api_version": "v2"}, # metadata.extra_data
    "tone": "analytical", # tweet.tone
    "topics": ["dict", "serialization"], # tweet.topics
    "sentiment_score": 0.75 # tweet.sentiment_score
}


RAW_AI_RESPONSE_DATA = {
    "content": "This is a dict-generated AI reply.",
    "response_type": "TWEET_REPLY", # String, will be converted to Enum
    "model_used": "test_model_v2_dict",
    "prompt_used": "Test prompt from dict",
    "generation_time": NOW_ISO,
    "source_tweet_id": "original_tweet_dict_456",
    "responding_as": "YieldFiInternDict",
    "target_account": "TargetUserDict",
    "tone": "neutral_dict",
    "max_length": 280,
    "temperature": 0.8,
    "feedback_score": 4.5,
    "feedback_comments": "Looks good from dict.",
    "was_used": True,
    "engagement_metrics": {"likes": 10, "retweets": 2},
    "tags": ["dict_test", "ai_reply"],
    "referenced_knowledge": ["doc_id_1", "faq_id_2"],
    "extra_context": {"user_segment": "advanced"},
    "image_url": "https://example.com/image_dict.png"
}

RAW_TWEET_CATEGORY_DATA = {
    "name": "Dict Product Update",
    "description": "Announcements about new product features from dict.",
    "prompt_keywords": ["new feature dict", "launch dict", "update dict"],
    "style_guidelines": {"tone": "informative_dict", "length": "concise_dict"}
}


# --- AccountType Tests ---
def test_account_type_from_string_valid():
    assert AccountType.from_string("Official") == AccountType.OFFICIAL
    assert AccountType.from_string("Intern") == AccountType.INTERN
    assert AccountType.from_string("Partner") == AccountType.PARTNER
    assert AccountType.from_string("KOL") == AccountType.KOL
    assert AccountType.from_string("Big Account") == AccountType.BIG_ACCOUNT
    assert AccountType.from_string("Community Member") == AccountType.COMMUNITY_MEMBER
    assert AccountType.from_string("Partner Intern") == AccountType.PARTNER_INTERN
    assert AccountType.from_string("Competitor") == AccountType.COMPETITOR
    assert AccountType.from_string("Institution") == AccountType.INSTITUTION
    assert AccountType.from_string("Unknown") == AccountType.UNKNOWN
    # Case-insensitivity
    assert AccountType.from_string("official") == AccountType.OFFICIAL
    assert AccountType.from_string("bIg AcCoUnT") == AccountType.BIG_ACCOUNT

def test_account_type_from_string_invalid():
    with pytest.raises(ValueError):
        AccountType.from_string("NonExistentType")

# --- Account Model Tests ---
def test_account_creation_minimal():
    acc = Account(account_id="min_id", username="min_user")
    assert acc.account_id == "min_id"
    assert acc.username == "min_user"
    assert acc.account_type == AccountType.UNKNOWN # Default
    assert acc.platform == "Twitter" # Default
    assert acc.follower_count is None

def test_account_creation_full():
    acc = Account(
        account_id="test_id_123",
        username="testuser",
        display_name="Test User",
        account_type=AccountType.OFFICIAL,
        platform="Twitter",
        follower_count=1000,
        bio="This is a test account.",
        interaction_history=[{"event": "followed"}],
        tags=["test", "pytest"],
        created_at=NOW_ISO # Storing as string, model might convert
    )
    assert acc.username == "testuser"
    assert acc.account_type == AccountType.OFFICIAL
    assert acc.interaction_history == [{"event": "followed"}]
    assert acc.created_at == NOW_ISO

def test_account_from_dict():
    data = copy.deepcopy(RAW_ACCOUNT_DATA)
    account = Account.from_dict(data)
    assert account.account_id == data["account_id"]
    assert account.username == data["username"]
    assert account.display_name == data["display_name"]
    assert account.account_type == AccountType.KOL
    assert account.platform == data["platform"]
    assert account.follower_count == data["follower_count"]
    assert account.verified == data["verified"]
    assert account.bio == data["bio"]
    assert account.created_at == data["created_at"] # Stays as string
    assert account.tags == data["tags"]

def test_account_from_dict_minimal_type():
    data = {"account_id": "min1", "username": "min_user1", "account_type": "Official"}
    account = Account.from_dict(data)
    assert account.account_type == AccountType.OFFICIAL

def test_account_from_dict_invalid_type_string_defaults_to_unknown():
    # from_dict for Account handles invalid string by defaulting to UNKNOWN and printing warning
    data = {"account_id": "inv_type", "username": "inv_user", "account_type": "NonExistent"}
    account = Account.from_dict(data)
    assert account.account_type == AccountType.UNKNOWN

def test_account_to_dict():
    account = Account.from_dict(copy.deepcopy(RAW_ACCOUNT_DATA))
    account_dict = account.to_dict()
    assert account_dict["account_id"] == RAW_ACCOUNT_DATA["account_id"]
    assert account_dict["username"] == RAW_ACCOUNT_DATA["username"]
    assert account_dict["account_type"] == RAW_ACCOUNT_DATA["account_type"] # Enum value
    assert account_dict["follower_count"] == RAW_ACCOUNT_DATA["follower_count"]
    assert account_dict["created_at"] == RAW_ACCOUNT_DATA["created_at"] # Should be ISO string

# --- TweetMetadata Model Tests ---
def test_tweet_metadata_creation_minimal():
    meta = TweetMetadata(source="test_source")
    assert meta.source == "test_source"
    assert meta.tweet_id is None
    assert meta.created_at is None
    assert meta.hashtags == [] # Default factory

def test_tweet_metadata_creation_full():
    meta = TweetMetadata(
        tweet_id="tweet123_full",
        created_at=NOW,
        source="TestSourceFull",
        author_id="author123_full",
        author_username="author_user_full",
        like_count=10,
        hashtags=["#full"]
    )
    assert meta.tweet_id == "tweet123_full"
    assert meta.created_at == NOW
    assert meta.hashtags == ["#full"]

# TweetMetadata doesn\'t have its own from_dict/to_dict, it\'s handled by Tweet model.
# We will test its serialization as part of Tweet tests.

# --- Tweet Model Tests ---
def test_tweet_creation_minimal():
    tweet = Tweet(content="Minimal tweet content")
    assert tweet.content == "Minimal tweet content"
    assert isinstance(tweet.metadata, TweetMetadata) # Default factory
    assert tweet.metadata.source == "manual" # Default from TweetMetadata
    assert tweet.tone is None

def test_tweet_creation_full():
    metadata = TweetMetadata(
        tweet_id="tweet123",
        created_at=NOW,
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
    assert tweet.metadata.created_at == NOW

def test_tweet_post_init_validation_empty_content():
    with pytest.raises(ValueError, match="Tweet content cannot be empty"):
        Tweet(content="")

def test_tweet_from_dict():
    data = copy.deepcopy(RAW_TWEET_DATA)
    tweet = Tweet.from_dict(data)
    
    assert tweet.content == data["content"]
    assert tweet.tone == data["tone"]
    assert tweet.topics == data["topics"]
    assert tweet.sentiment_score == data["sentiment_score"]
    
    # Test metadata part
    assert tweet.metadata.tweet_id == data["id"]
    assert tweet.metadata.created_at == NOW # Datetime object
    assert tweet.metadata.source == data["source"]
    assert tweet.metadata.author_id == data["author_id"]
    assert tweet.metadata.author_username == data["author_username"]
    assert tweet.metadata.like_count == data["like_count"]
    assert tweet.metadata.hashtags == data["hashtags"]
    assert tweet.metadata.extra_data == data["extra_data"]

def test_tweet_from_dict_missing_required_fields():
    with pytest.raises(KeyError, match="'id'"):
        Tweet.from_dict({"content": "no id"})
    with pytest.raises(KeyError, match="'content'"):
        Tweet.from_dict({"id": "no_content_id"})

def test_tweet_from_dict_datetime_parsing_zulu():
    data_zulu = copy.deepcopy(RAW_TWEET_DATA)
    data_zulu["created_at"] = "2023-01-01T12:00:00Z"
    tweet = Tweet.from_dict(data_zulu)
    assert tweet.metadata.created_at == datetime(2023, 1, 1, 12, 0, 0, tzinfo=timezone.utc)

def test_tweet_to_dict():
    tweet = Tweet.from_dict(copy.deepcopy(RAW_TWEET_DATA))
    tweet_dict = tweet.to_dict()

    assert tweet_dict["content"] == RAW_TWEET_DATA["content"]
    assert tweet_dict["tone"] == RAW_TWEET_DATA["tone"]
    assert tweet_dict["topics"] == RAW_TWEET_DATA["topics"]

    meta_dict = tweet_dict["metadata"]
    assert meta_dict["tweet_id"] == RAW_TWEET_DATA["id"]
    assert meta_dict["created_at"] == NOW_ISO # Check ISO format
    assert meta_dict["source"] == RAW_TWEET_DATA["source"]
    assert meta_dict["author_username"] == RAW_TWEET_DATA["author_username"]
    assert meta_dict["hashtags"] == RAW_TWEET_DATA["hashtags"]

# --- ResponseType Enum Tests ---
def test_response_type_enum_access():
    assert ResponseType.TWEET_REPLY.name == "TWEET_REPLY"
    # Value is auto-generated, so we check type
    assert isinstance(ResponseType.TWEET_REPLY.value, int)

# --- AIResponse Model Tests ---
def test_ai_response_creation_minimal():
    response = AIResponse(
        content="Minimal AI response.",
        response_type=ResponseType.CUSTOM,
        model_used="min_model"
    )
    assert response.content == "Minimal AI response."
    assert response.response_type == ResponseType.CUSTOM
    assert response.model_used == "min_model"
    assert isinstance(response.generation_time, datetime) # Default factory
    assert response.tags == [] # Default factory

def test_ai_response_creation_full():
    response = AIResponse(
        content="This is a generated reply.",
        response_type=ResponseType.TWEET_REPLY,
        model_used="test_model_v1",
        prompt_used="Test prompt",
        generation_time=NOW,
        source_tweet_id="original_tweet_123",
        responding_as="YieldFiOfficial",
        target_account="TargetUser",
        tone="positive",
        image_url="http://example.com/img.png"
    )
    assert response.response_type == ResponseType.TWEET_REPLY
    assert response.model_used == "test_model_v1"
    assert response.generation_time == NOW
    assert response.image_url == "http://example.com/img.png"

def test_ai_response_post_init_validation_empty_content():
    with pytest.raises(ValueError, match="Response content cannot be empty"):
        AIResponse(content="", response_type=ResponseType.NEW_TWEET, model_used="test")

def test_ai_response_from_dict():
    data = copy.deepcopy(RAW_AI_RESPONSE_DATA)
    response = AIResponse.from_dict(data)

    assert response.content == data["content"]
    assert response.response_type == ResponseType.TWEET_REPLY # Enum
    assert response.model_used == data["model_used"]
    assert response.generation_time == NOW # Datetime object
    assert response.source_tweet_id == data["source_tweet_id"]
    assert response.tone == data["tone"]
    assert response.feedback_score == data["feedback_score"]
    assert response.engagement_metrics == data["engagement_metrics"]
    assert response.image_url == data["image_url"]

def test_ai_response_from_dict_response_type_handling():
    data_custom = copy.deepcopy(RAW_AI_RESPONSE_DATA)
    data_custom["response_type"] = "NON_EXISTENT_TYPE"
    response_custom = AIResponse.from_dict(data_custom)
    assert response_custom.response_type == ResponseType.CUSTOM

    data_none = copy.deepcopy(RAW_AI_RESPONSE_DATA)
    data_none["response_type"] = None
    response_none = AIResponse.from_dict(data_none)
    assert response_none.response_type == ResponseType.CUSTOM
    
    data_new = copy.deepcopy(RAW_AI_RESPONSE_DATA)
    data_new["response_type"] = "NEW_TWEET"
    response_new = AIResponse.from_dict(data_new)
    assert response_new.response_type == ResponseType.NEW_TWEET

def test_ai_response_to_dict():
    response = AIResponse.from_dict(copy.deepcopy(RAW_AI_RESPONSE_DATA))
    response_dict = response.to_dict()

    assert response_dict["content"] == RAW_AI_RESPONSE_DATA["content"]
    assert response_dict["response_type"] == RAW_AI_RESPONSE_DATA["response_type"] # Enum name
    assert response_dict["model_used"] == RAW_AI_RESPONSE_DATA["model_used"]
    assert response_dict["generation_time"] == NOW_ISO # Check ISO format
    assert response_dict["tone"] == RAW_AI_RESPONSE_DATA["tone"]
    assert response_dict["image_url"] == RAW_AI_RESPONSE_DATA["image_url"]

# --- TweetCategory Model Tests ---
def test_tweet_category_creation_minimal():
    category = TweetCategory(name="Minimal Cat", description="Min Desc")
    assert category.name == "Minimal Cat"
    assert category.description == "Min Desc"
    assert category.prompt_keywords == [] # Default
    assert category.style_guidelines == {} # Default

def test_tweet_category_creation_full():
    category = TweetCategory(
        name="Product Update Full",
        description="Announcements about new product features or releases.",
        prompt_keywords=["new feature", "launch", "update"],
        style_guidelines={"tone": "informative", "length": "concise"}
    )
    assert category.name == "Product Update Full"
    assert "launch" in category.prompt_keywords
    assert category.style_guidelines["tone"] == "informative"

def test_tweet_category_from_dict():
    data = copy.deepcopy(RAW_TWEET_CATEGORY_DATA)
    category = TweetCategory.from_dict(data)
    assert category.name == data["name"]
    assert category.description == data["description"]
    assert category.prompt_keywords == data["prompt_keywords"]
    assert category.style_guidelines == data["style_guidelines"]

# TweetCategory doesn\'t have a to_dict method, not typically needed for this model.
# If it were added, tests would go here.

def test_load_categories_function_from_category_module(tmp_path):
    """ Test the load_categories function from src.models.category """
    from src.models.category import load_categories
    
    # Create a dummy categories.json
    categories_content = [
        RAW_TWEET_CATEGORY_DATA,
        {
            "name": "Community", 
            "description": "Community related tweets",
            "prompt_keywords": ["ama", "feedback"],
            "style_guidelines": {"tone": "friendly"}
        }
    ]
    
    # Mock get_config to return a path within tmp_path
    mock_input_dir = tmp_path / "data" / "input"
    mock_input_dir.mkdir(parents=True, exist_ok=True)
    categories_file = mock_input_dir / "categories.json"
    
    with open(categories_file, 'w') as f:
        import json
        json.dump(categories_content, f)

    # Patch get_config to control the path
    with patch('src.models.category.get_config') as mock_get_config:
        mock_get_config.return_value = str(mock_input_dir)
        
        loaded_cats = load_categories() # Uses patched get_config path
        assert len(loaded_cats) == 2
        assert loaded_cats[0].name == RAW_TWEET_CATEGORY_DATA["name"]
        assert loaded_cats[1].name == "Community"
        assert "ama" in loaded_cats[1].prompt_keywords

    # Test with explicit path
    loaded_cats_explicit = load_categories(categories_file_path=str(categories_file))
    assert len(loaded_cats_explicit) == 2
    assert loaded_cats_explicit[0].description == RAW_TWEET_CATEGORY_DATA["description"]

    # Test file not found
    with patch('src.models.category.get_config') as mock_get_config:
        mock_get_config.return_value = str(tmp_path / "non_existent_dir")
        assert load_categories() == [] # Expect empty list and printed error

    # Test invalid JSON
    invalid_json_file = mock_input_dir / "invalid_categories.json"
    with open(invalid_json_file, 'w') as f:
        f.write("{not_a_list: true}")
    assert load_categories(categories_file_path=str(invalid_json_file)) == []

    # Test empty JSON file
    empty_json_file = mock_input_dir / "empty_categories.json"
    with open(empty_json_file, 'w') as f:
        f.write("[]") # Empty list is valid
    assert load_categories(categories_file_path=str(empty_json_file)) == []
    with open(empty_json_file, 'w') as f: # Truly empty
        f.write("")
    assert load_categories(categories_file_path=str(empty_json_file)) == [] # prints error, returns [] 