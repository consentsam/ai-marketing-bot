# API Documentation

This document describes the programmatic APIs provided by the YieldFi AI Agent project. It covers configuration utilities, data models, data sources, AI modules, knowledge interfaces, and evaluation tools.

---
## 1. Configuration API

### src/config/settings.py

- `load_config() -> dict`
  • Loads `config.yaml` and overrides with environment variables (via `.env` and direct `os.environ`).

- `get_config(key_path: str, default: Any = None) -> Any`
  • Retrieves a configuration value using dot-notation (e.g., `ai.xai_api_key`).
  • Returns `default` if the key is not found.

**Environment Variables:**
- `XAI_API_KEY`: xAI API key.
- `GOOGLE_API_KEY`: Google PaLM API key (fallback).
- `AI__USE_FALLBACK`: Flag to force PaLM fallback (true/false).
- Base URLs: `AI__XAI_BASE_URL`, `AI__GOOGLE_PALM_BASE_URL`
- Defaults: `AI__DEFAULT_MAX_TOKENS`, `AI__DEFAULT_TEMPERATURE`
- `DEFAULT_PROTOCOL`: Default protocol for categories and knowledge (e.g., "ethena").
- `GROK_IMAGE_API_KEY`: API key for poster image generation feature.

---
## 2. Models API

### src/models/account.py
```python
class AccountType(Enum):
    OFFICIAL = "OFFICIAL"
    INTERN = "INTERN"
    PARTNER = "PARTNER"
    KOL = "KOL"
    INSTITUTION = "INSTITUTION"
    COMMUNITY_MEMBER = "COMMUNITY_MEMBER"
    PARTNER_INTERN = "PARTNER_INTERN"
    COMPETITOR = "COMPETITOR"
    UNKNOWN = "UNKNOWN"

    @classmethod
    def from_string(cls, s: str) -> AccountType
        """Convert a string to an AccountType enum."""
```
```python
dataclass
class Account:
    account_id: str
    username: str
    display_name: str
    account_type: AccountType
    platform: str
    follower_count: int
    bio: Optional[str]
    interaction_history: List[Any]
    tags: List[str]

    @classmethod
    def from_dict(cls, data: dict) -> Account
    def to_dict(self) -> dict
```

### src/models/tweet.py
```python
dataclass
class TweetMetadata:
    tweet_id: str
    created_at: datetime
    source: Optional[str]
    author_id: str
    author_username: str
    like_count: Optional[int]
    reply_count: Optional[int]
    retweet_count: Optional[int]
    in_reply_to_tweet_id: Optional[str]

    @classmethod
    def from_dict(cls, data: dict) -> TweetMetadata
    def to_dict(self) -> dict
```
```python
dataclass
class Tweet:
    content: str
    metadata: TweetMetadata
    tone: Optional[str]
    topics: List[str]
    sentiment_score: Optional[float]

    @classmethod
    def from_dict(cls, data: dict) -> Tweet
    def to_dict(self) -> dict
```

### src/models/response.py
```python
dataclass
class AIResponse:
    content: str
    response_type: ResponseType
    model_used: str
    prompt_used: Optional[str]
    source_tweet_id: Optional[str]
    responding_as: Optional[str]
    target_account: Optional[str]
    generation_time: datetime
    tone: Optional[str]
    image_url: Optional[str] = None  # URL to a generated poster image
    max_length: Optional[int]
    temperature: Optional[float]
    feedback_score: Optional[float]
    feedback_comments: Optional[str]
    was_used: Optional[bool]
    engagement_metrics: Dict[str, Any]
    tags: List[str]
    referenced_knowledge: List[str]
    extra_context: Dict[str, Any]
```

### src/models/category.py
```python
@dataclass
class TweetCategory:
    name: str
    description: str
    prompt_keywords: List[str]
    style_guidelines: Dict[str, str]

    @classmethod
    def from_dict(cls, data: dict) -> TweetCategory
    def to_dict(self) -> dict
    
    @staticmethod
    def load_categories(file_path: Optional[str] = None) -> List[TweetCategory]
        """Load categories from a JSON file. Uses data_paths.input from config if file_path is None."""
```

---
## 3. Data Sources API

### src/data_sources/base.py
```python
class TweetDataSource(ABC):
    @property
    def name(self) -> str: ...
    @property
    def is_read_only(self) -> bool: ...
    def get_tweet_by_id(self, tweet_id: str) -> Tweet: ...
    def get_tweet_by_url(self, url: str) -> Tweet: ...
    def search_tweets(self, query: str) -> List[Tweet]: ...
    def get_account_info(self, account_id: str) -> Account: ...
    def get_account_by_username(self, username: str) -> Account: ...
    def get_recent_tweets_by_account(self, account_id: str) -> List[Tweet]: ...
    def post_tweet(self, tweet: Tweet) -> str: ...
```

### src/data_sources/mock.py
```python
class MockTweetDataSource(TweetDataSource):
    def __init__(self, tweets_file: str, accounts_file: str)
    def get_tweet_by_id(self, tweet_id: str) -> Tweet
    ... # implements all abstract methods using local JSON
```

---
## 4. AI Client & Prompt API

### src/ai/xai_client.py
```python
class XAIClient:
    def __init__(self, api_key: Optional[str] = None, google_api_key: Optional[str] = None)
    def get_completion(self, prompt: str, max_tokens: int = None, temperature: float = None, **kwargs) -> dict
        Raises APIError on request or HTTP failures.
```

### src/ai/prompt_engineering.py
```python
get_base_yieldfi_persona(account_type: AccountType) -> str
get_instruction_set(active_account_type: AccountType, target_account_type: Optional[AccountType]) -> str

def generate_interaction_prompt(
    original_tweet: Tweet,
    responding_as_account: Account,
    target_account: Optional[Account] = None,
    yieldfi_knowledge_snippet: Optional[str] = None,
    interaction_details: Optional[Dict[str, Any]] = None,
    platform: str = "Twitter"
) -> str

def generate_new_tweet_prompt(
    category: TweetCategory,
    active_account: Account,
    topic: Optional[str] = None,
    yieldfi_knowledge_snippet: Optional[str] = None,
    platform: str = "Twitter"
) -> str
```

### src/ai/tone_analyzer.py
```python
def analyze_tone(text: str, method: Optional[str] = None) -> Dict[str, Any]
    # returns {'tone': str, 'sentiment_score': float, 'subjectivity': float, 'confidence': float}

def analyze_tweet_tone(tweet: Tweet) -> Tweet
```

### src/ai/response_generator.py
```python
def generate_tweet_reply(
    original_tweet: Tweet,
    responding_as: Account,
    target_account: Optional[Account] = None,
    platform: str = "Twitter",
    interaction_details: Optional[Dict[str, Any]] = None,
    knowledge_retriever: Optional[KnowledgeRetriever] = None,
    generate_image: bool = False
) -> AIResponse

def generate_new_tweet(
    category: TweetCategory,
    responding_as: Account,
    topic: Optional[str] = None,
    platform: str = "Twitter",
    additional_instructions: Optional[Dict[str, Any]] = None,
    knowledge_retriever: Optional[KnowledgeRetriever] = None,
    generate_image: bool = False
) -> AIResponse
```

### src/ai/image_generation.py
```python
def get_poster_image(prompt: str) -> str
    """
    Generates or retrieves a poster image for the given prompt.
    
    Args:
        prompt: The prompt or text to generate an image for.
        
    Returns:
        A URL string pointing to the generated image.
    """
    # Uses GROK_IMAGE_API_KEY from config or environment
    # Falls back to placeholder URL if no API key or on error
```

---
## 5. Knowledge API

### src/knowledge/base.py
```python
class KnowledgeSource(ABC):
    @property
    def name(self) -> str: ...
    def search(self, query: str, top_k: int = 5) -> List[RelevantChunk]

dataclass
class RelevantChunk:
    content: str
    source_name: str
    score: float
    metadata: dict
```

### src/knowledge/yieldfi.py
```python
class StaticJSONKnowledgeSource(KnowledgeSource):
    def __init__(self, file_path: Optional[str] = None)
    def search(self, query: str, top_k: int = 5) -> List[RelevantChunk]

class YieldFiDocsKnowledgeSource(KnowledgeSource):
    def __init__(self, file_path: Optional[str] = None)
    def search(self, query: str, top_k: int = 5) -> List[RelevantChunk]
```

---
## 6. Evaluation API

### src/evaluation/metrics.py
```python
def jaccard_similarity(text1: str, text2: str) -> float

def relevance_score(response_text: str, reference_text: str) -> float

def tone_adherence_score(detected_tone: str, desired_tone: str) -> float

def engagement_potential(response_text: str) -> float

def factual_accuracy_score(*args, **kwargs) -> float  # raises NotImplementedError
```

### src/evaluation/evaluator.py
```python
class Evaluator:
    def evaluate_response(
        self,
        response: AIResponse,
        reference: str,
        desired_tone: Optional[str] = None,
        allow_factual: bool = False
    ) -> Dict[str, float]
```

---
## 7. UI Components

### src/ui/tweet_input.py
```python
def display_tweet_reply_ui(active_account_type: AccountType)
    """Display UI for generating tweet replies."""
    # Creates input fields for tweet URL or content
    # Option to generate a poster image with "Generate Poster Image" checkbox
    # Calls response_generator.generate_tweet_reply() with generate_image flag
    # Displays generated content and image if requested
```

### src/ui/category_select.py
```python
def load_tweet_categories(file_path: str = DATA_CATEGORIES_PATH) -> List[TweetCategory]
    """Loads tweet categories from a JSON file, with caching for performance."""

def display_tone_badge(tone: Optional[str], prefix: str = "Tone: ")
    """Display a colored badge for the tone of a tweet or response."""

def display_category_tweet_ui(active_account_type: AccountType)
    """Display UI for selecting a category and generating a new tweet."""
    # Creates dropdown for selecting tweet category
    # Shows expanded view of category details
    # Option to generate a poster image 
    # Calls response_generator.generate_new_tweet() with generate_image flag
``` 

---
## Usage Example (Python)
```python
from src.ai.xai_client import XAIClient
from src.ai.prompt_engineering import generate_interaction_prompt
from src.ai.image_generation import get_poster_image
from src.models.account import Account, AccountType
from src.models.tweet import Tweet, TweetMetadata

# Generate text reply
client = XAIClient()
metadata = TweetMetadata(tweet_id="t1", created_at=datetime.now(), author_id="u1", author_username="user1")
tweet = Tweet(content="Hello World!", metadata=metadata)
prompt = generate_interaction_prompt(tweet, responding_as_account=Account(...))
response = client.get_completion(prompt)

# Generate image for tweet
image_url = get_poster_image("Create a visual for YieldFi's latest update on high APY rates")
``` 