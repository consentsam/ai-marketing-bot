"""
AI Response data models.

This module defines the data structures for representing AI-generated responses.
"""

from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, Dict, Any, List
from enum import Enum, auto


class ResponseType(Enum):
    """Types of AI-generated responses."""
    
    TWEET_REPLY = auto()         # Reply to a tweet
    NEW_TWEET = auto()           # New standalone tweet
    ANNOUNCEMENT = auto()        # Formal announcement
    PRODUCT_UPDATE = auto()      # Update about YieldFi products
    COMMUNITY_UPDATE = auto()    # Update about YieldFi community
    EVENT = auto()               # Event announcement or recap
    EDUCATIONAL = auto()         # Educational content about DeFi/YieldFi
    CUSTOM = auto()              # Custom response type


@dataclass
class AIResponse:
    """Representation of an AI-generated response."""
    
    # The generated content
    content: str
    
    # Type of response
    response_type: ResponseType
    
    # Metadata about the generation process
    model_used: str  # e.g., "xai-1.0", "gpt-4", etc.
    prompt_used: Optional[str] = None
    generation_time: datetime = field(default_factory=datetime.now)
    
    # Context that led to this response
    source_tweet_id: Optional[str] = None
    responding_as: Optional[str] = None  # e.g., "official", "intern"
    target_account: Optional[str] = None
    
    # Parameters used for generation
    tone: Optional[str] = None  # e.g., "professional", "casual", "excited"
    max_length: Optional[int] = None
    temperature: Optional[float] = None
    
    # Feedback and metrics
    feedback_score: Optional[float] = None
    feedback_comments: Optional[str] = None
    was_used: Optional[bool] = None  # Whether this response was actually used
    engagement_metrics: Dict[str, Any] = field(default_factory=dict)
    
    # Tags for categorization
    tags: List[str] = field(default_factory=list)
    
    # Referenced YieldFi knowledge
    referenced_knowledge: List[str] = field(default_factory=list)
    
    # Additional contextual information
    extra_context: Dict[str, Any] = field(default_factory=dict)
    
    def __post_init__(self):
        """Validate response after initialization."""
        if not self.content:
            raise ValueError("Response content cannot be empty")
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'AIResponse':
        """Create an AIResponse instance from a dictionary.
        
        Args:
            data: Dictionary containing response data
            
        Returns:
            A new AIResponse instance
        """
        # Handle response type conversion
        response_type = data.get('response_type')
        if isinstance(response_type, str):
            try:
                response_type = ResponseType[response_type.upper()]
            except KeyError:
                response_type = ResponseType.CUSTOM
        elif response_type is None:
            response_type = ResponseType.CUSTOM
        
        # Handle generation time
        generation_time = data.get('generation_time')
        if isinstance(generation_time, str):
            generation_time = datetime.fromisoformat(generation_time)
        elif generation_time is None:
            generation_time = datetime.now()
        
        return cls(
            content=data['content'],
            response_type=response_type,
            model_used=data.get('model_used', 'unknown'),
            prompt_used=data.get('prompt_used'),
            generation_time=generation_time,
            source_tweet_id=data.get('source_tweet_id'),
            responding_as=data.get('responding_as'),
            target_account=data.get('target_account'),
            tone=data.get('tone'),
            max_length=data.get('max_length'),
            temperature=data.get('temperature'),
            feedback_score=data.get('feedback_score'),
            feedback_comments=data.get('feedback_comments'),
            was_used=data.get('was_used'),
            engagement_metrics=data.get('engagement_metrics', {}),
            tags=data.get('tags', []),
            referenced_knowledge=data.get('referenced_knowledge', []),
            extra_context=data.get('extra_context', {})
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the AIResponse to a dictionary.
        
        Returns:
            Dictionary representation of the response
        """
        return {
            'content': self.content,
            'response_type': self.response_type.name,
            'model_used': self.model_used,
            'prompt_used': self.prompt_used,
            'generation_time': self.generation_time.isoformat(),
            'source_tweet_id': self.source_tweet_id,
            'responding_as': self.responding_as,
            'target_account': self.target_account,
            'tone': self.tone,
            'max_length': self.max_length,
            'temperature': self.temperature,
            'feedback_score': self.feedback_score,
            'feedback_comments': self.feedback_comments,
            'was_used': self.was_used,
            'engagement_metrics': self.engagement_metrics,
            'tags': self.tags,
            'referenced_knowledge': self.referenced_knowledge,
            'extra_context': self.extra_context
        } 