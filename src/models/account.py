# Changelog:
# 2025-05-07 HH:MM - Step 2 - Validated existing AccountType and Account models against plan. Ensured from_dict/to_dict and docstrings are present. Noted pre-existing additional fields and enum members.
# 2025-05-06 HH:MM - Initial review - Structure aligns well with roadmap requirements.

"""
Account data models.

This module defines the data structures for representing social media accounts and their types,
crucial for context-aware AI responses across different platforms like Twitter, Discord, etc.
Rationale: Standardized account representation is needed for consistent processing and
           tailoring AI interactions based on account roles and platforms.
Usage: Instantiated by data source modules when fetching account information and used by
       the AI core to determine appropriate communication strategies.
TODOs:
    - Consider adding a field for 'last_seen' or 'last_interacted' if tracking active community members becomes a priority.
"""

from dataclasses import dataclass, field
from enum import Enum
from typing import Optional, Dict, Any, List # Removed 'auto' as it's not used for string-valued enums here


class AccountType(Enum):
    """Types of social media accounts for context-aware responses."""
    
    # YieldFi account types
    OFFICIAL = "Official"           # Official YieldFi account
    INTERN = "Intern"               # YieldFi intern account
    
    # External account types
    PARTNER = "Partner"             # Partner organization
    KOL = "KOL"                     # Key Opinion Leader / Influencer
    BIG_ACCOUNT = "Big Account"     # Generic large, influential account (can overlap with KOL)
    COMMUNITY_MEMBER = "Community Member" # Regular community member
    PARTNER_INTERN = "Partner Intern" # Intern for partner organizations
    COMPETITOR = "Competitor"       # Competitor in the DeFi space
    INSTITUTION = "Institution"     # For 'OfficialToInstitution' interactions
    UNKNOWN = "Unknown"             # Default type for unclassified accounts
    
    @classmethod
    def from_string(cls, value: str) -> 'AccountType':
        """Convert a string to an AccountType. Handles spaces by replacing with underscores for enum member matching."""
        try:
            # Normalize the input string to match enum member names (e.g., "Big Account" -> "BIG_ACCOUNT")
            normalized_value = value.upper().replace(" ", "_")
            return cls[normalized_value]
        except KeyError:
            # Fallback for direct value matching if normalization fails (e.g. "Official" matches OFFICIAL.value)
            for member in cls:
                if member.value.upper() == value.upper():
                    return member
            # If still not found, consider it UNKNOWN or raise error
            # For robustness, we can default to UNKNOWN if an exact match isn't critical for all cases.
            # However, for specific context handling, an error might be better.
            # Given the current usage, raising ValueError is appropriate.
            # print(f"Warning: Unknown account type string '{value}'. Defaulting to UNKNOWN.") # Optional warning
            # return cls.UNKNOWN
            raise ValueError(f"Unknown account type string: '{value}'. Cannot map to AccountType enum.")


@dataclass
class Account:
    """Representation of a social media account."""
    
    # Basic account information
    account_id: str # Platform-specific ID
    username: str   # Platform-specific username (e.g., @handle for Twitter)
    display_name: Optional[str] = None
    
    # Account classification
    account_type: AccountType = AccountType.UNKNOWN
    platform: str = "Twitter" # e.g., "Twitter", "Discord", "Telegram" - Default to Twitter for now
    
    # Account metrics (primarily for Twitter, might vary for other platforms)
    follower_count: Optional[int] = None
    following_count: Optional[int] = None
    verified: bool = False
    
    # YieldFi relationship (can be expanded)
    is_following_yieldfi: bool = False # If applicable for the platform
    followed_by_yieldfi: bool = False  # If applicable for the platform
    
    # Historical interaction data with the YieldFi agent/brand
    interaction_history: List[Dict[str, Any]] = field(default_factory=list) # e.g., previous DMs, replies
    
    # Additional metadata
    bio: Optional[str] = None
    location: Optional[str] = None
    website: Optional[str] = None
    created_at: Optional[str] = None # Platform-specific account creation date string
    
    # Custom notes or tags for this account by the agent/team
    tags: List[str] = field(default_factory=list) # e.g., ["potential_lead", "vocal_critic"]
    notes: Optional[str] = None
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> 'Account':
        """Create an Account instance from a dictionary."""
        account_type_str = data.get('account_type')
        resolved_account_type = AccountType.UNKNOWN
        if isinstance(account_type_str, str):
            try:
                resolved_account_type = AccountType.from_string(account_type_str)
            except ValueError:
                # Log this warning if a logger is available here, or handle as needed
                print(f"Warning: Could not map account_type '{account_type_str}' to enum. Defaulting to UNKNOWN for account_id '{data.get('account_id')}'.")
                resolved_account_type = AccountType.UNKNOWN
        elif account_type_str is None: # Explicitly handle None if it can occur
            resolved_account_type = AccountType.UNKNOWN
        
        return cls(
            account_id=data['account_id'],
            username=data['username'],
            display_name=data.get('display_name'),
            account_type=resolved_account_type,
            platform=data.get('platform', "Twitter"), # Default to Twitter if not specified
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
        """Convert the Account to a dictionary."""
        return {
            'account_id': self.account_id,
            'username': self.username,
            'display_name': self.display_name,
            'account_type': self.account_type.value, # Store the string value
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