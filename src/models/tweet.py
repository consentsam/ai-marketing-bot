"""
Tweet data models.

This module defines the data structures for representing tweets and their metadata.

# Changelog:
# 2025-05-07 HH:MM - Step 2 - Validated existing Tweet and TweetMetadata models. Ensured from_dict/to_dict (handled via nested Tweet methods) and docstrings are present. Noted pre-existing additional fields.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any


@dataclass
class TweetMetadata:
    """Metadata associated with a tweet."""
    
    # Tweet source information
    tweet_id: Optional[str] = None
    created_at: Optional[datetime] = None
    source: str = "manual"  # Can be "twitter", "manual", etc.
    
    # Author information
    author_id: Optional[str] = None
    author_username: Optional[str] = None
    author_name: Optional[str] = None
    author_verified: bool = False
    author_follower_count: Optional[int] = None
    
    # Engagement metrics
    like_count: Optional[int] = None
    retweet_count: Optional[int] = None
    reply_count: Optional[int] = None
    quote_count: Optional[int] = None
    
    # Context
    in_reply_to_tweet_id: Optional[str] = None
    in_reply_to_user_id: Optional[str] = None
    mentioned_users: List[str] = field(default_factory=list)
    hashtags: List[str] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)
    
    # Additional data that might be source-specific
    extra_data: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Tweet:
    """Representation of a tweet with content and metadata."""
    
    # The main content of the tweet
    content: str
    
    # Associated metadata
    metadata: TweetMetadata = field(default_factory=TweetMetadata)
    
    # Analysis results (to be filled by processing modules)
    tone: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    sentiment_score: Optional[float] = None
    
    def __post_init__(self):
        """Perform validation after initialization."""
        if not self.content:
            raise ValueError("Tweet content cannot be empty")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Tweet':
        """Create a Tweet instance from a dictionary representation.
        
        This is useful when loading tweets from JSON files or APIs.
        
        Args:
            data: Dictionary containing tweet data
            
        Returns:
            A new Tweet instance
        """
        # Check for required fields
        if 'id' not in data:
            raise KeyError('id')
        if 'content' not in data:
            raise KeyError('content')

        created_at_str = data.get('created_at')
        created_at_dt = None
        if created_at_str:
            if created_at_str.endswith('Z'):
                created_at_str = created_at_str[:-1] + '+00:00'
            created_at_dt = datetime.fromisoformat(created_at_str)

        metadata = TweetMetadata(
            tweet_id=data.get('id'),
            created_at=created_at_dt,
            source=data.get('source', 'manual'),
            author_id=data.get('author_id'),
            author_username=data.get('author_username'),
            author_name=data.get('author_name'),
            author_verified=data.get('author_verified', False),
            author_follower_count=data.get('author_follower_count'),
            like_count=data.get('like_count'),
            retweet_count=data.get('retweet_count'),
            reply_count=data.get('reply_count'),
            quote_count=data.get('quote_count'),
            in_reply_to_tweet_id=data.get('in_reply_to_tweet_id'),
            in_reply_to_user_id=data.get('in_reply_to_user_id'),
            mentioned_users=data.get('mentioned_users', []),
            hashtags=data.get('hashtags', []),
            urls=data.get('urls', []),
            extra_data=data.get('extra_data', {})
        )
        
        return cls(
            content=data['content'],
            metadata=metadata,
            tone=data.get('tone'),
            topics=data.get('topics', []),
            sentiment_score=data.get('sentiment_score')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the Tweet to a dictionary representation.
        
        Returns:
            Dictionary representation of the tweet
        """
        result = {
            'content': self.content,
            'tone': self.tone,
            'topics': self.topics,
            'sentiment_score': self.sentiment_score,
            'metadata': {
                'tweet_id': self.metadata.tweet_id,
                'created_at': self.metadata.created_at.isoformat() if self.metadata.created_at else None,
                'source': self.metadata.source,
                'author_id': self.metadata.author_id,
                'author_username': self.metadata.author_username,
                'author_name': self.metadata.author_name,
                'author_verified': self.metadata.author_verified,
                'author_follower_count': self.metadata.author_follower_count,
                'like_count': self.metadata.like_count,
                'retweet_count': self.metadata.retweet_count,
                'reply_count': self.metadata.reply_count,
                'quote_count': self.metadata.quote_count,
                'in_reply_to_tweet_id': self.metadata.in_reply_to_tweet_id,
                'in_reply_to_user_id': self.metadata.in_reply_to_user_id,
                'mentioned_users': self.metadata.mentioned_users,
                'hashtags': self.metadata.hashtags,
                'urls': self.metadata.urls,
                'extra_data': self.metadata.extra_data
            }
        }
        return result 