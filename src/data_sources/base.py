"""
Base classes for tweet data sources.

This module defines the abstract interface for tweet data sources. Any implementation
of a tweet data source must implement this interface.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any, Optional

from src.models.tweet import Tweet
from src.models.account import Account


class TweetDataSource(ABC):
    """Abstract base class for tweet data sources.
    
    This class defines the interface that all tweet data sources must implement.
    Concrete implementations might include Twitter API, manual input, or other sources.
    """
    
    @abstractmethod
    def get_tweet_by_id(self, tweet_id: str) -> Optional[Tweet]:
        """Retrieve a tweet by its ID.
        
        Args:
            tweet_id: The unique identifier of the tweet
            
        Returns:
            The Tweet object if found, otherwise None
        """
        pass
    
    @abstractmethod
    def get_tweet_by_url(self, url: str) -> Optional[Tweet]:
        """Retrieve a tweet by its URL.
        
        Args:
            url: The URL pointing to the tweet
            
        Returns:
            The Tweet object if found, otherwise None
        """
        pass
    
    @abstractmethod
    def search_tweets(self, query: str, limit: int = 10) -> List[Tweet]:
        """Search for tweets matching the given query.
        
        Args:
            query: The search query
            limit: Maximum number of tweets to return
            
        Returns:
            List of Tweet objects matching the query
        """
        pass
    
    @abstractmethod
    def get_account_info(self, account_id: str) -> Optional[Account]:
        """Get information about a Twitter account.
        
        Args:
            account_id: The unique identifier of the account
            
        Returns:
            The Account object if found, otherwise None
        """
        pass
    
    @abstractmethod
    def get_account_by_username(self, username: str) -> Optional[Account]:
        """Get information about a Twitter account by username.
        
        Args:
            username: The username of the account
            
        Returns:
            The Account object if found, otherwise None
        """
        pass
    
    @abstractmethod
    def get_recent_tweets_by_account(self, account_id: str, limit: int = 10) -> List[Tweet]:
        """Get recent tweets from a specific account.
        
        Args:
            account_id: The unique identifier of the account
            limit: Maximum number of tweets to return
            
        Returns:
            List of recent Tweet objects from the account
        """
        pass
    
    @abstractmethod
    def post_tweet(self, content: str, reply_to: Optional[str] = None) -> Optional[str]:
        """Post a new tweet or reply to an existing tweet.
        
        Args:
            content: The content of the tweet
            reply_to: The ID of the tweet to reply to (if any)
            
        Returns:
            The ID of the posted tweet if successful, otherwise None
        """
        pass
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Get the name of this data source.
        
        Returns:
            The name of the data source
        """
        pass
    
    @property
    @abstractmethod
    def is_read_only(self) -> bool:
        """Check if this data source is read-only.
        
        Returns:
            True if the data source is read-only, False otherwise
        """
        pass
    
    @property
    @abstractmethod
    def capabilities(self) -> Dict[str, bool]:
        """Get the capabilities of this data source.
        
        Returns:
            Dictionary of capability names and whether they are supported
        """
        pass 