import pytest
from datetime import datetime
from src.models.account import AccountType
from src.models.tweet import Tweet
from src.models.response import AIResponse


def test_account_type_from_string_variants():
    # valid with spaces and case-insensitive
    assert AccountType.from_string("Big Account") == AccountType.BIG_ACCOUNT
    assert AccountType.from_string("big account") == AccountType.BIG_ACCOUNT
    assert AccountType.from_string("KOL") == AccountType.KOL


def test_account_type_from_string_invalid_raises():
    # unknown string should raise ValueError
    with pytest.raises(ValueError):
        AccountType.from_string("NonexistentType")


def test_airesponse_from_dict_with_datetime():
    now = datetime.utcnow()
    data = {
        "content": "test content",
        "response_type": "TWEET_REPLY",
        "model_used": "model_x",
        "generation_time": now
    }
    resp = AIResponse.from_dict(data)
    assert resp.generation_time == now


def test_tweet_from_dict_defaults_minimal():
    data = {"id": "t1", "content": "hello world"}
    tweet = Tweet.from_dict(data)
    # metadata defaults
    assert tweet.metadata.created_at is None
    assert tweet.metadata.source == "manual"
    assert tweet.metadata.extra_data == {}
    # tweet defaults
    assert tweet.topics == []
    assert tweet.sentiment_score is None


def test_tweet_from_dict_invalid_created_at():
    data = {"id": "t1", "content": "hello world", "created_at": "invalid-date"}
    with pytest.raises(ValueError):
        Tweet.from_dict(data)
