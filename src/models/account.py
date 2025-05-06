"""
Account data models.

This module defines the data structures for representing Twitter accounts and their types.
"""

from dataclasses import dataclass, field
from enum import Enum, auto
from typing import Optional, Dict, Any, List


class AccountType(Enum):
    """Types of Twitter accounts for context-aware responses."""
    
    # YieldFi account types
    OFFICIAL = "Official"          # Official YieldFi account
    INTERN = "Intern"              # YieldFi intern account
    PARTNER = "Partner"            # Partner organization
    BIG_ACCOUNT = "Big Account"     # Influencer with large following
    KOL = "KOL"                    # Key Opinion Leader
    PARTNER_INTERN = "Partner Intern"  # Intern for partner organizations
    COMMUNITY_MEMBER = "Community Member"  # Regular community member
    COMPETITOR = "Competitor"      # Competitor in the DeFi space
    UNKNOWN = "Unknown"            # Default type for unclassified accounts
    
    @classmethod
    def from_string(cls, value: str) -> 'AccountType':
        """Convert a string to an AccountType.
        
        Args:
            value: String representation of account type
            
        Returns:
            AccountType enum value
            
        Raises:
            ValueError: If the string doesn't match any AccountType
        """
        try:
            return cls[value.upper().replace(" ", "_")]
        except KeyError:
            raise ValueError(f"Unknown account type: {value}")


@dataclass
class Account:
    """Representation of a Twitter account."""
    
    # Basic account information
    account_id: str
    username: str
    display_name: Optional[str] = None
    
    # Account classification
    account_type: AccountType = AccountType.UNKNOWN
    
    # Platform information
    platform: str  # e.g., "Twitter", "Discord", "Telegram"
    
    # Account metrics
    follower_count: Optional[int] = None
    following_count: Optional[int] = None
    verified: bool = False
    
    # YieldFi relationship
    is_following_yieldfi: bool = False
    followed_by_yieldfi: bool = False
    
    # Historical interaction data
    interaction_history: List[Dict[str, Any]] = field(default_factory=list)
    
    # Additional metadata
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    created_at: Optional[str] = None
    
    # Custom notes or tags for this account
    tags: List[str] = field(default_factory=list)
    notes: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Account':
        """Create an Account instance from a dictionary.
        
        Args:
            data: Dictionary containing account data
            
        Returns:
            A new Account instance
        """
        # Convert string account type to enum
        account_type = data.get('account_type')
        if isinstance(account_type, str):
            try:
                account_type = AccountType.from_string(account_type)
            except ValueError:
                account_type = AccountType.UNKNOWN
        elif account_type is None:
            account_type = AccountType.UNKNOWN
        
        return cls(
            account_id=data['account_id'],
            username=data['username'],
            display_name=data.get('display_name'),
            account_type=account_type,
            platform=data.get('platform', "Unknown"),  # Default to "Unknown" if not provided
            follower_count=data.get('follower_count'),
            following_count=data.get('following_count'),
            verified=data.get('verified', False),
            is_following_yieldfi=data.get('is_following_yieldfi', False),
            followed_by_yieldfi=data.get('followed_by_yieldfi', False),
            interaction_history=data.get('interaction_history', []),
            bio=data.get('bio'),
            location=data.get('location'),
            website=data.get('website'),
            created_at=data.get('created_at'),
            tags=data.get('tags', []),
            notes=data.get('notes')
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the Account to a dictionary.
        
        Returns:
            Dictionary representation of the account
        """
        return {
            'account_id': self.account_id,
            'username': self.username,
            'display_name': self.display_name,
            'account_type': self.account_type.name,
            'platform': self.platform,
            'follower_count': self.follower_count,
            'following_count': self.following_count,
            'verified': self.verified,
            'is_following_yieldfi': self.is_following_yieldfi,
            'followed_by_yieldfi': self.followed_by_yieldfi,
            'interaction_history': self.interaction_history,
            'bio': self.bio,
            'location': self.location,
            'website': self.website,
            'created_at': self.created_at,
            'tags': self.tags,
            'notes': self.notes
        } 