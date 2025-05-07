# Changelog:
# 2025-05-07 HH:MM - Step 4 (Testing) - Initial test structure for MockTweetDataSource.

import unittest
from unittest.mock import patch, mock_open
import os
import json
from datetime import datetime

from src.data_sources.mock import MockTweetDataSource
from src.models.tweet import Tweet, TweetMetadata
from src.models.account import Account, AccountType

class TestMockTweetDataSource(unittest.TestCase):

    _sample_accounts_data = [
        {
            "account_id": "user1", "username": "TestUser1", "display_name": "Test User One", 
            "account_type": "Community Member", "platform": "Twitter", "follower_count": 100,
            "bio": "Bio for user1", "interaction_history": [], "tags": ["test"]
        },
        {
            "account_id": "user2", "username": "TestUser2", "display_name": "Test User Two",
            "account_type": "Partner", "platform": "Twitter", "follower_count": 200,
            "bio": "Bio for user2", "interaction_history": [], "tags": ["partner", "test"]
        }
    ]
    _sample_tweets_data = [
        {
            "id": "tweet1", "content": "Hello world from user1", "created_at": "2023-01-01T12:00:00Z",
            "source": "Twitter Web App", "author_id": "user1", "author_username": "TestUser1",
            "like_count": 10, "reply_count": 1
        },
        {
            "id": "tweet2", "content": "Another tweet, this is from user2 about #test", "created_at": "2023-01-02T12:00:00Z",
            "source": "Twitter for iPhone", "author_id": "user2", "author_username": "TestUser2",
            "like_count": 20, "hashtags": ["test"]
        },
        {
            "id": "tweet3", "content": "A reply to tweet1 from user2", "created_at": "2023-01-03T12:00:00Z",
            "source": "Twitter Web App", "author_id": "user2", "author_username": "TestUser2",
            "in_reply_to_tweet_id": "tweet1", "like_count": 5
        }
    ]

    @patch("os.path.exists")
    @patch("builtins.open", new_callable=mock_open)
    def setUp(self, mock_file_open_param, mock_path_exists_param):
        # Default behavior for mocks
        mock_path_exists_param.return_value = True
        
        # Configure mock_open for accounts and tweets
        # This simulates different content for different file paths
        def mock_file_open_side_effect(file_path, *args, **kwargs):
            if "sample_accounts.json" in file_path:
                return mock_open(read_data=json.dumps(self._sample_accounts_data))()
            elif "sample_tweets.json" in file_path:
                return mock_open(read_data=json.dumps(self._sample_tweets_data))()
            else:
                # Default mock_open behavior for other files if any
                return mock_open()()

        mock_file_open_param.side_effect = mock_file_open_side_effect
        
        self.data_source = MockTweetDataSource(data_dir="dummy_dir")

    def test_load_accounts(self):
        self.assertEqual(len(self.data_source._accounts), 2 * 2) # Indexed by ID and username
        self.assertIn("user1", self.data_source._accounts)
        self.assertIn("testuser1", self.data_source._accounts) # Lowercase username
        self.assertIsInstance(self.data_source._accounts["user1"], Account)
        self.assertEqual(self.data_source._accounts["user1"].username, "TestUser1")
        self.assertEqual(self.data_source._accounts["user1"].account_type, AccountType.COMMUNITY_MEMBER)

    def test_load_tweets(self):
        self.assertEqual(len(self.data_source._tweets), 3)
        self.assertIn("tweet1", self.data_source._tweets)
        self.assertIsInstance(self.data_source._tweets["tweet1"], Tweet)
        self.assertEqual(self.data_source._tweets["tweet1"].content, "Hello world from user1")
        self.assertEqual(self.data_source._tweets["tweet1"].metadata.author_id, "user1")

    def test_get_tweet_by_id(self):
        tweet = self.data_source.get_tweet_by_id("tweet1")
        self.assertIsNotNone(tweet)
        self.assertEqual(tweet.content, "Hello world from user1")
        self.assertIsNone(self.data_source.get_tweet_by_id("nonexistent_tweet"))

    def test_get_account_by_username(self):
        account = self.data_source.get_account_by_username("TestUser1")
        self.assertIsNotNone(account)
        self.assertEqual(account.account_id, "user1")
        self.assertIsNone(self.data_source.get_account_by_username("nonexistent_user"))

    def test_search_tweets(self):
        results = self.data_source.search_tweets("user2")
        self.assertEqual(len(results), 2)
        self.assertTrue(any(t.metadata.tweet_id == "tweet2" for t in results))
        self.assertTrue(any(t.metadata.tweet_id == "tweet3" for t in results))

        results_hashtag = self.data_source.search_tweets("#test")
        self.assertEqual(len(results_hashtag), 1)
        self.assertEqual(results_hashtag[0].metadata.tweet_id, "tweet2")
        
        results_limit = self.data_source.search_tweets("tweet", limit=1)
        self.assertEqual(len(results_limit), 1)

    def test_get_recent_tweets_by_account(self):
        results = self.data_source.get_recent_tweets_by_account("user2", limit=5)
        self.assertEqual(len(results), 2)
        self.assertEqual(results[0].metadata.tweet_id, "tweet3") # Most recent
        self.assertEqual(results[1].metadata.tweet_id, "tweet2")

    def test_post_tweet(self):
        original_tweet_count = len(self.data_source._tweets)
        new_tweet_content = "This is a new test tweet!"
        new_tweet_id = self.data_source.post_tweet(new_tweet_content)
        
        self.assertIsNotNone(new_tweet_id)
        self.assertEqual(len(self.data_source._tweets), original_tweet_count + 1)
        posted_tweet = self.data_source.get_tweet_by_id(new_tweet_id)
        self.assertIsNotNone(posted_tweet)
        self.assertEqual(posted_tweet.content, new_tweet_content)
        self.assertEqual(posted_tweet.metadata.author_username, "mock_user") # As per mock impl

    def test_properties(self):
        self.assertEqual(self.data_source.name, "Mock Twitter Data Source")
        self.assertFalse(self.data_source.is_read_only)
        expected_capabilities = {
            "get_tweet": True, "search_tweets": True, "get_account": True,
            "get_recent_tweets": True, "post_tweet": True, "streaming": False,
            "media_upload": False, "direct_messages": False
        }
        self.assertEqual(self.data_source.capabilities, expected_capabilities)

    # New tests for data loading and edge cases

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_load_tweets_file_not_found(self, mock_path_exists, mock_file_open):
        mock_path_exists.return_value = False # Simulate file not found
        data_source = MockTweetDataSource(data_dir="non_existent_dir")
        self.assertEqual(len(data_source._tweets), 0)

    @patch("builtins.open", new_callable=mock_open)
    @patch("os.path.exists")
    def test_load_accounts_file_not_found(self, mock_path_exists, mock_file_open):
        mock_path_exists.return_value = False # Simulate file not found
        data_source = MockTweetDataSource(data_dir="non_existent_dir")
        self.assertEqual(len(data_source._accounts), 0)

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    @patch("os.path.exists", return_value=True)
    def test_load_tweets_empty_file(self, mock_path_exists, mock_file_open):
        # mock_file_open is already configured with read_data="[]"
        data_source = MockTweetDataSource(data_dir="dummy_dir_empty_tweets")
        self.assertEqual(len(data_source._tweets), 0)

    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    @patch("os.path.exists", return_value=True)
    def test_load_accounts_empty_file(self, mock_path_exists, mock_file_open):
        data_source = MockTweetDataSource(data_dir="dummy_dir_empty_accounts")
        self.assertEqual(len(data_source._accounts), 0)

    @patch("builtins.print") # To capture error print
    @patch("builtins.open", new_callable=mock_open, read_data="this is not json")
    @patch("os.path.exists", return_value=True)
    def test_load_tweets_malformed_json(self, mock_path_exists, mock_file_open, mock_print):
        data_source = MockTweetDataSource(data_dir="dummy_dir_malformed_tweets")
        self.assertEqual(len(data_source._tweets), 0)
        mock_print.assert_any_call(f"Error loading tweets from dummy_dir_malformed_tweets/sample_tweets.json: Expecting value: line 1 column 1 (char 0)")

    @patch("builtins.print")
    @patch("builtins.open", new_callable=mock_open, read_data="not a valid json account")
    @patch("os.path.exists", return_value=True)
    def test_load_accounts_malformed_json(self, mock_path_exists, mock_file_open, mock_print):
        data_source = MockTweetDataSource(data_dir="dummy_dir_malformed_accounts")
        self.assertEqual(len(data_source._accounts), 0)
        mock_print.assert_any_call(f"Error loading accounts from dummy_dir_malformed_accounts/sample_accounts.json: Expecting value: line 1 column 1 (char 0)")

    @patch("builtins.print")
    @patch("os.path.exists", return_value=True)
    def test_load_tweets_missing_required_fields(self, mock_path_exists, mock_print):
        # Tweet missing 'content'
        tweets_missing_content = [{ "id": "tweet_no_content", "created_at": "2023-01-01T12:00:00Z", "author_id": "user1" }]
        # Tweet missing 'id'
        tweets_missing_id = [{ "content": "Valid content", "created_at": "2023-01-01T12:00:00Z", "author_id": "user1" }]
        
        with patch("builtins.open", mock_open(read_data=json.dumps(tweets_missing_content))):
            data_source = MockTweetDataSource(data_dir="dummy_missing_content")
            self.assertEqual(len(data_source._tweets), 0)
            mock_print.assert_any_call("Error loading tweet: 'content'") # KeyError for content

        mock_print.reset_mock() # Reset mock for next part of test
        with patch("builtins.open", mock_open(read_data=json.dumps(tweets_missing_id))):
            data_source = MockTweetDataSource(data_dir="dummy_missing_id")
            self.assertEqual(len(data_source._tweets), 0)
            # The error from Tweet.from_dict for missing 'id' would be a TypeError when trying to access metadata.tweet_id, 
            # or if metadata.tweet_id is None and then used as a key. It depends on the exact Tweet.from_dict logic.
            # Let's assume it prints an error. A more robust check would be specific to the expected error.
            # For now, checking if *any* error related to loading that specific tweet was printed.
            # This will depend on the actual error message which might be 'id' directly or related to None being used as key.
            # The current mock.py prints KeyError or ValueError, so missing 'id' in source dict should be KeyError.
            mock_print.assert_any_call("Error loading tweet: 'id'") 

    @patch("builtins.print")
    @patch("os.path.exists", return_value=True)
    def test_load_accounts_missing_required_fields(self, mock_path_exists, mock_print):
        # Account missing 'account_id'
        account_missing_id = [{ "username": "user_no_id", "account_type": "Community Member"}]
        # Account missing 'username'
        account_missing_username = [{ "account_id": "acc_no_user", "account_type": "Partner"}]

        with patch("builtins.open", mock_open(read_data=json.dumps(account_missing_id))):
            data_source = MockTweetDataSource(data_dir="dummy_acc_missing_id")
            self.assertEqual(len(data_source._accounts), 0)
            mock_print.assert_any_call("Error loading account: 'account_id'")

        mock_print.reset_mock() 
        with patch("builtins.open", mock_open(read_data=json.dumps(account_missing_username))):
            data_source = MockTweetDataSource(data_dir="dummy_acc_missing_username")
            self.assertEqual(len(data_source._accounts), 0)
            mock_print.assert_any_call("Error loading account: 'username'")

    def test_get_recent_tweets_by_non_existent_account(self):
        # Uses the default setUp for data_source instance
        results = self.data_source.get_recent_tweets_by_account("non_existent_user_id", limit=5)
        self.assertEqual(len(results), 0)

    def test_search_tweets_empty_query(self):
        # Uses the default setUp for data_source instance
        # Current mock implementation returns all tweets if query is empty or part of any content.
        # For an empty query, it might match all if not handled specifically.
        # Let's assume an empty query should return no results for stricter search.
        # This test might fail based on current MockTweetDataSource.search_tweets logic
        # and might require adjusting that logic or this test assertion.
        # For now, testing current behavior: an empty query would be in any content string
        # if `query in tweet.content.lower()` and query is empty. Python's `"" in "abc"` is True.
        # So, current search_tweets would return all tweets.
        # We will adjust test to expect all tweets, or adjust search_tweets to return empty for empty query.
        # Sticking to testing existing behavior for now.
        results = self.data_source.search_tweets("", limit=10)
        self.assertEqual(len(results), len(self._sample_tweets_data)) # Expects all tweets

    def test_search_tweets_no_match(self):
        results = self.data_source.search_tweets("query_that_will_not_match_anything_123xyz", limit=10)
        self.assertEqual(len(results), 0)

if __name__ == '__main__':
    unittest.main() 