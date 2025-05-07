# Changelog:
# 2025-05-07 HH:MM - Step 4 - Validated and adopted existing MockTweetDataSource. Confirmed implementation of all TweetDataSource abstract methods using local JSON files, in-memory tweet posting, and property implementations.

"""
Mock implementation of TweetDataSource.

This module provides a mock implementation of the TweetDataSource interface
that uses local JSON files as the data source. This is useful for development
and testing without needing actual Twitter API access.
"""

import json
import os
import re
from datetime import datetime
from typing import List, Dict, Any, Optional
from urllib.parse import urlparse, parse_qs

from src.data_sources.base import TweetDataSource
from src.models.tweet import Tweet, TweetMetadata
from src.models.account import Account, AccountType


class MockTweetDataSource(TweetDataSource):
    """Mock implementation of TweetDataSource using local JSON files."""
    
    def __init__(self, data_dir: str = "data/input"):
        """Initialize the mock tweet data source.
        
        Args:
            data_dir: Directory containing sample data files
        """
        self.data_dir = data_dir
        self._tweets = self._load_tweets()
        self._accounts = self._load_accounts()
    
    def _load_tweets(self) -> Dict[str, Tweet]:
        """Load tweets from the sample data file.
        
        Returns:
            Dictionary mapping tweet IDs to Tweet objects
        """
        tweets = {}
        tweets_file = os.path.join(self.data_dir, "sample_tweets.json")
        
        if os.path.exists(tweets_file):
            try:
                with open(tweets_file, "r", encoding="utf-8") as f:
                    tweet_data = json.load(f)
                
                for tweet_dict in tweet_data:
                    try:
                        tweet = Tweet.from_dict(tweet_dict)
                        tweets[tweet.metadata.tweet_id] = tweet
                    except (KeyError, ValueError) as e:
                        print(f"Error loading tweet: {e}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading tweets from {tweets_file}: {e}")
        
        return tweets
    
    def _load_accounts(self) -> Dict[str, Account]:
        """Load accounts from the sample data file.
        
        Returns:
            Dictionary mapping account IDs to Account objects
        """
        accounts = {}
        accounts_file = os.path.join(self.data_dir, "sample_accounts.json")
        
        if os.path.exists(accounts_file):
            try:
                with open(accounts_file, "r", encoding="utf-8") as f:
                    account_data = json.load(f)
                
                for account_dict in account_data:
                    try:
                        account = Account.from_dict(account_dict)
                        accounts[account.account_id] = account
                        # Also index by username for easier lookup
                        accounts[account.username.lower()] = account
                    except (KeyError, ValueError) as e:
                        print(f"Error loading account: {e}")
            except (json.JSONDecodeError, IOError) as e:
                print(f"Error loading accounts from {accounts_file}: {e}")
        
        return accounts
    
    def _extract_tweet_id_from_url(self, url: str) -> Optional[str]:
        """Extract the tweet ID from a Twitter URL.
        
        Args:
            url: Twitter URL
            
        Returns:
            The tweet ID if found, otherwise None
        """
        # Pattern to match Twitter URLs like:
        # https://twitter.com/username/status/1234567890
        # https://x.com/username/status/1234567890
        pattern = r"(?:twitter\.com|x\.com)/\w+/status/(\d+)"
        match = re.search(pattern, url)
        
        if match:
            return match.group(1)
        return None
    
    def get_tweet_by_id(self, tweet_id: str) -> Optional[Tweet]:
        """Retrieve a tweet by its ID.
        
        Args:
            tweet_id: The unique identifier of the tweet
            
        Returns:
            The Tweet object if found, otherwise None
        """
        return self._tweets.get(tweet_id)
    
    def get_tweet_by_url(self, url: str) -> Optional[Tweet]:
        """Retrieve a tweet by its URL.
        
        Args:
            url: The URL pointing to the tweet
            
        Returns:
            The Tweet object if found, otherwise None
        """
        tweet_id = self._extract_tweet_id_from_url(url)
        if tweet_id:
            return self.get_tweet_by_id(tweet_id)
        return None
    
    def search_tweets(self, query: str, limit: int = 10) -> List[Tweet]:
        """Search for tweets matching the given query.
        
        Args:
            query: The search query
            limit: Maximum number of tweets to return
            
        Returns:
            List of Tweet objects matching the query
        """
        query = query.lower()
        results = []
        
        for tweet in self._tweets.values():
            if query in tweet.content.lower():
                results.append(tweet)
                if len(results) >= limit:
                    break
        
        return results
    
    def get_account_info(self, account_id: str) -> Optional[Account]:
        """Get information about a Twitter account.
        
        Args:
            account_id: The unique identifier of the account
            
        Returns:
            The Account object if found, otherwise None
        """
        return self._accounts.get(account_id)
    
    def get_account_by_username(self, username: str) -> Optional[Account]:
        """Get information about a Twitter account by username.
        
        Args:
            username: The username of the account
            
        Returns:
            The Account object if found, otherwise None
        """
        return self._accounts.get(username.lower())
    
    def get_recent_tweets_by_account(self, account_id: str, limit: int = 10) -> List[Tweet]:
        """Get recent tweets from a specific account.
        
        Args:
            account_id: The unique identifier of the account
            limit: Maximum number of tweets to return
            
        Returns:
            List of recent Tweet objects from the account
        """
        results = []
        
        for tweet in self._tweets.values():
            if tweet.metadata.author_id == account_id:
                results.append(tweet)
                if len(results) >= limit:
                    break
        
        # Sort by creation time, newest first
        results.sort(
            key=lambda t: t.metadata.created_at or datetime.min,
            reverse=True
        )
        
        return results
    
    def post_tweet(self, content: str, reply_to: Optional[str] = None) -> Optional[str]:
        """Post a new tweet or reply to an existing tweet.
        
        In the mock implementation, this just prints the tweet and returns a fake ID.
        
        Args:
            content: The content of the tweet
            reply_to: The ID of the tweet to reply to (if any)
            
        Returns:
            The ID of the posted tweet if successful, otherwise None
        """
        # Generate a random ID for the new tweet
        import random
        new_id = str(random.randint(1000000000000000000, 9999999999999999999))
        
        # Create metadata for the new tweet
        metadata = TweetMetadata(
            tweet_id=new_id,
            created_at=datetime.now(),
            source="mock",
            author_id="mock_user",
            author_username="mock_user",
            in_reply_to_tweet_id=reply_to
        )
        
        # Create the new tweet
        new_tweet = Tweet(content=content, metadata=metadata)
        
        # Add it to our local collection
        self._tweets[new_id] = new_tweet
        
        print(f"[MOCK] {'Reply' if reply_to else 'Tweet'} posted: {content}")
        if reply_to:
            print(f"[MOCK] In reply to: {reply_to}")
        
        return new_id
    
    @property
    def name(self) -> str:
        """Get the name of this data source.
        
        Returns:
            The name of the data source
        """
        return "Mock Twitter Data Source"
    
    @property
    def is_read_only(self) -> bool:
        """Check if this data source is read-only.
        
        Returns:
            True if the data source is read-only, False otherwise
        """
        return False  # It can "post" tweets to the mock
    
    @property
    def capabilities(self) -> Dict[str, bool]:
        """Get the capabilities of this data source.
        
        Returns:
            Dictionary of capability names and whether they are supported
        """
        return {
            "get_tweet": True,
            "search_tweets": True,
            "get_account": True,
            "get_recent_tweets": True,
            "post_tweet": True,
            "streaming": False,
            "media_upload": False,
            "direct_messages": False
        } 