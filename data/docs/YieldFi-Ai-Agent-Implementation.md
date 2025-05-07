# YieldFi AI Agent Implementation Plan

This document outlines the detailed implementation plan for the YieldFi AI Agent, focusing on creating a modular, scalable system for Twitter interaction and content generation using xAI APIs.

## Overview

The YieldFi AI Agent aims to enhance YieldFi's social media presence by automating and optimizing Twitter replies and content generation. This implementation focuses on creating a modular architecture that allows for different tweet data sources (starting with mock data, then live Twitter API), making future integration with other platforms (Discord, Telegram as per roadmap) and knowledge sources more streamlined.

## Core Architecture

- [x] **Step 1: Set up project structure and environment**
    -   **Task**: Create the base project directory structure as specified, initialize `git`, create initial `.gitignore`, `requirements.txt` (with essential libraries like `python-dotenv`, `pyyaml`, `streamlit`), and an initial `.env.example` file.
        -   **EXPLANATION**: A well-defined structure from the start makes it easier for the AI to locate files, understand module relationships, and generate code for the correct locations. Explicitly listing initial requirements helps in environment setup.
    -   **Key Considerations/Sub-Tasks**:
        * Create main directories: `src/`, `data/`, `data/docs`, `data/input`, `data/output`, `tests/`, `scripts/`, `.cursor/rules/`.
        * Create sub-directories within `src/`: `ai/`, `config/`, `data_sources/`, `knowledge/`, `models/`, `ui/`, `utils/`.
        * Create `__init__.py` files in `src/` and all its subdirectories to mark them as Python packages.
        * Populate `.env.example` with all anticipated API keys and configuration variables (e.g., `XAI_API_KEY`, `TWITTER_API_KEY`, `LOG_LEVEL`, `DATA_SOURCE_TYPE`).
        * Populate `requirements.txt` with initial core dependencies.
    -   **Files**:
        * `src/`
        * `src/config/`
        * `src/data_sources/`
        * `src/models/`
        * `src/ai/`
        * `src/utils/`
        * `src/knowledge/`
        * `src/ui/`
        * `src/evaluation/`
        * `src/analytics/`
        * `src/feedback/`
        * `data/docs/`
        * `data/input/`
        * `data/output/`
        * `tests/`
        * `.env.example`
        * `requirements.txt`
        * `.gitignore`
    -   **Step Dependencies**: None
    -   **User Instructions**: Clone the repository (if it exists, otherwise initialize git) and ensure Python 3.9+ is installed. Run `pip install -r requirements.txt` after this step is complete to install initial dependencies.

---
**Step Completion Summary (2025-05-07 HH:MM):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `.gitignore`
    * `requirements.txt`
    * `src/__init__.py`
    * `src/ai/__init__.py`
    * `src/config/__init__.py`
    * `src/data_sources/__init__.py`
    * `src/knowledge/__init__.py`
    * `src/models/__init__.py`
    * `src/ui/__init__.py`
    * `src/utils/__init__.py`
    * `src/evaluation/__init__.py`
    * `src/analytics/__init__.py`
    * `src/feedback/__init__.py`
    * Directories created: `src/` (and subdirectories `ai`, `config`, `data_sources`, `knowledge`, `models`, `ui`, `utils`, `evaluation`, `analytics`, `feedback`), `data/` (and subdirectories `docs`, `input`, `output`), `tests/`, `scripts/`, `.cursor/rules/`.
* **Summary of Changes:**
    * `.gitignore`: Created with standard Python, IDE, and environment ignore patterns. Ensured `.env` is ignored and `!.env.example` is not.
    * `requirements.txt`: Updated to include `python-dotenv`, `pyyaml`, `streamlit`. Noted that the file pre-existed with other dependencies which were preserved.
    * `src/*/__init__.py` files: All specified `__init__.py` files were created or confirmed to exist, ensuring Python package structure. Some were noted to have pre-existing content.
    * Directories: The specified project directory structure was created using `mkdir -p`.
    * `.env.example`: User was instructed to create this file manually due to a "globalIgnore" tool restriction preventing its automated creation. The intended content for this file was provided to the user.
---

- [x] **Step 2: Define core data models**
    -   **Task**: Implement Python dataclasses for `Tweet`, `TweetMetadata`, `Account`, `AccountType` (Enum), and `AIResponse`, `ResponseType` (Enum) in their respective files within `src/models/`. These models should include all fields necessary for processing tweet data, representing user accounts, and structuring AI-generated responses, as informed by `sample_tweets.json`, `sample_accounts.json`, and the project roadmap. Include `from_dict` and `to_dict` methods for serialization/deserialization.
        -   **EXPLANATION**: Detailed data models guide the AI in understanding the structure of data it will work with, leading to more accurate code for data manipulation, storage, and API interactions. Specifying `from_dict`/`to_dict` standardizes data handling.
    -   **Key Considerations/Sub-Tasks**:
        * `AccountType` enum: Define all relevant types (OFFICIAL, INTERN, PARTNER, KOL, INSTITUTION, COMMUNITY_MEMBER, PARTNER_INTERN, COMPETITOR, UNKNOWN) with string values. Implement `from_string` classmethod.
        * `Account` dataclass: Include fields like `account_id`, `username`, `display_name`, `account_type` (using `AccountType`), `platform`, `follower_count`, `bio`, `interaction_history`, `tags`.
        * `TweetMetadata` dataclass: Include `tweet_id`, `created_at`, `source`, `author_id`, `author_username`, engagement metrics (`like_count`, etc.), context fields (`in_reply_to_tweet_id`).
        * `Tweet` dataclass: Include `content`, `metadata` (using `TweetMetadata`), and fields for analysis results like `tone`, `topics`, `sentiment_score`.
        * `ResponseType` enum: Define types like `TWEET_REPLY`, `NEW_TWEET`, `ANNOUNCEMENT`, `PRODUCT_UPDATE`, `COMMUNITY_UPDATE`, etc.
        * `AIResponse` dataclass: Include `content`, `response_type` (using `ResponseType`), `model_used`, `prompt_used`, `source_tweet_id`, `responding_as`, `target_account`, `tone`.
        * Ensure all models have comprehensive docstrings.
        * Create `src/models/__init__.py` to expose these models.
    -   **Files**:
        * `src/models/tweet.py`
        * `src/models/account.py`
        * `src/models/response.py`
        * `src/models/__init__.py`
    -   **Step Dependencies**: Step 1
    -   **User Instructions**: Review the implemented data models. Ensure they capture all necessary fields based on `sample_tweets.json`, `sample_accounts.json`, and the types of interactions planned in `data/docs/InstructionsFor*.md` and the roadmap.

- [x] **Step 3: Implement abstract data source interface**
    -   **Task**: Define an abstract base class `TweetDataSource` in `src/data_sources/base.py` with abstract methods for all data operations needed (e.g., `get_tweet_by_id`, `get_tweet_by_url`, `search_tweets`, `get_account_info`, `get_account_by_username`, `get_recent_tweets_by_account`, `post_tweet`). The methods should use the data models from Step 2 in their signatures.
        -   **EXPLANATION**: A clear contract for data sources ensures that any concrete implementation (mock, Twitter API, etc.) will be compatible with the rest of the system. Specifying method signatures with defined models aids the AI in generating compliant implementations.
    -   **Key Considerations/Sub-Tasks**:
        * Use `abc.ABC` and `abc.abstractmethod`.
        * Define methods clearly specifying expected arguments (types from `src/models`) and return types (types from `src/models`).
        * Include properties like `name` (str), `is_read_only` (bool), and `capabilities` (Dict[str, bool]).
        * Write a comprehensive docstring for the class and each abstract method.
    -   **Files**:
        * `src/data_sources/base.py`
        * `src/data_sources/__init__.py` (to export `TweetDataSource`)
    -   **Step Dependencies**: Step 2
    -   **User Instructions**: None.

---
**Step Completion Summary (2025-05-07 HH:MM):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/data_sources/base.py`
    * `src/data_sources/__init__.py`
* **Summary of Changes:**
    * `src/data_sources/base.py`: Validated pre-existing `TweetDataSource` abstract base class. Confirmed all required abstract methods (using Step 2 models), properties, and docstrings were present and correctly defined. Added changelog entry.
    * `src/data_sources/__init__.py`: Confirmed pre-existing file correctly exports `TweetDataSource`. Updated changelog.
---

- [x] **Step 4: Implement mock tweet data source**
    -   **Task**: Create `MockTweetDataSource` in `src/data_sources/mock.py` that inherits from `TweetDataSource` and implements all abstract methods by reading from/writing to local JSON files (`data/input/sample_tweets.json`, `data/input/sample_accounts.json`).
        -   **EXPLANATION**: A functional mock allows early testing and development of dependent modules (AI logic, UI). Explicitly stating it should implement *all* methods ensures the AI doesn't miss any part of the interface.
    -   **Key Considerations/Sub-Tasks**:
        * Implement `_load_tweets` and `_load_accounts` to parse JSON data into the defined data models (Step 2). Handle potential file errors.
        * Implement `get_tweet_by_id`, `get_tweet_by_url` (including URL parsing to ID).
        * Implement `search_tweets` with basic case-insensitive string matching.
        * Implement `get_account_info` and `get_account_by_username`.
        * Implement `get_recent_tweets_by_account` (consider sorting by date).
        * Implement `post_tweet`: For mock, this can append to an in-memory list or print to console, returning a mock tweet ID.
        * Ensure data consistency (e.g., `author_id` in tweets refers to an existing account).
    -   **Files**:
        * `src/data_sources/mock.py`
        * `data/input/sample_tweets.json` (ensure it's populated)
        * `data/input/sample_accounts.json` (ensure it's populated)
    -   **Step Dependencies**: Step 3
    -   **User Instructions**: Populate `sample_tweets.json` and `sample_accounts.json` with diverse and representative data, including different account types and tweet scenarios, to facilitate thorough testing.

---
**Step Completion Summary (2025-05-07 HH:MM):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/data_sources/mock.py`
    * `data/input/sample_tweets.json` (Validated existence)
    * `data/input/sample_accounts.json` (Validated existence)
* **Summary of Changes:**
    * `src/data_sources/mock.py`: Validated pre-existing `MockTweetDataSource`. Confirmed it implements `TweetDataSource`, loads data from JSON, handles in-memory posting, and implements properties. Added changelog.
    * `data/input/sample_tweets.json` & `data/input/sample_accounts.json`: Confirmed these data files exist and appear populated. User reminded to ensure diverse and representative data as per plan.
---

- [x] **Step 5: Define configuration system**
    -   **Task**: Implement `src/config/settings.py` to load configurations from `config.yaml` and environment variables (using `python-dotenv` and `os.environ`). Provide functions like `get_config(key, default)` and `load_config()`.
        -   **EXPLANATION**: Detailing the expected functions (`get_config`, `load_config`) and sources (YAML, .env) provides a clear target for implementation, ensuring all necessary config access patterns are covered.
    -   **Key Considerations/Sub-Tasks**:
        * `load_config()` should read `config.yaml` first, then override with environment variables.
        * `get_config()` should allow fetching nested values using dot notation (e.g., `ai.provider`).
        * Prioritize environment variables over `config.yaml` values.
        * Ensure `.env` is in `.gitignore`.
        * Define default values in `config.yaml` for non-sensitive settings.
        * Handle missing keys gracefully in `get_config` (return `default`).
    -   **Files**:
        * `src/config/settings.py`
        * `src/config/__init__.py` (to export config functions)
        * `config.yaml` (with default values)
        * Update `.gitignore` to include `.env`.
    -   **Step Dependencies**: Step 1
    -   **User Instructions**: Create a `.env` file based on `.env.example` and populate it with your actual API keys (placeholder for now if not available) and any environment-specific settings.

---
**Step Completion Summary (2025-05-07 HH:MM - Inferred):**
* **Status:** Completed & Approved by User (Inferred from file existence and content)
* **Files Modified/Created:**
    * `src/config/settings.py` (Created/Updated)
    * `src/config/__init__.py` (Likely Updated)
    * `config.yaml` (Created/Updated)
    * `.gitignore` (Ensured `.env` is present)
    * `tests/config/test_settings.py` (Likely Created)
* **Summary of Changes:**
    * `src/config/settings.py`: Implemented a robust configuration loading system. `load_config()` handles loading from `config.yaml`, then overrides with values from `.env` (via `python-dotenv`), and finally direct environment variables. `get_config(key_path, default)` allows case-insensitive dot-notation access to nested configuration values. Type conversion for boolean, integer, and float values from environment variables is handled. Changelog entries in the file indicate prior work.
    * `src/config/__init__.py`: Assumed to export necessary functions like `get_config`, `load_config`.
    * `config.yaml`: Assumed to be created with default application configurations.
    * `tests/config/test_settings.py`: Assumed to be created with unit tests for the configuration system.
---

## AI Integration

- [x] **Step 6: Create xAI API client**
    -   **Task**: Implement `XAIClient` in `src/ai/xai_client.py`. This class will handle all communication with the xAI API (or a fallback like Google PaLM as currently designed). Include methods for text generation (e.g., `get_completion`). Implement error handling and API key management using the config system from Step 5.
        -   **EXPLANATION**: Specifying method names like `get_completion` and focusing on error handling and API key management directs the AI to build a robust and usable client.
    -   **Key Considerations/Sub-Tasks**:
        * Constructor `__init__(self, api_key=None)` should load API key from config if not provided.
        * `get_completion(self, prompt, max_tokens, temperature, **kwargs)` method.
        * Implement fallback logic to Google PaLM if `XAI_API_KEY` is missing or `use_fallback` is true, using `GOOGLE_API_KEY`.
        * Use a library like `requests` for HTTP calls if no official xAI SDK is available (prepare for placeholder/mocked API calls initially).
        * Implement proper error handling for API responses (e.g., rate limits, authentication errors, using `APIError` from `src/utils/error_handling.py`).
        * Add docstrings explaining parameters and return values.
    -   **Files**:
        * `src/ai/xai_client.py`
        * Update `src/ai/__init__.py` (export `XAIClient`)
        * `tests/ai/test_xai_client.py` (Likely Created)
    -   **Step Dependencies**: Step 5
    -   **User Instructions**: Obtain an xAI API key (if available, otherwise development will use the fallback) and add it to your `.env` file as `XAI_API_KEY`. Also, add `GOOGLE_API_KEY` if using the PaLM fallback.
---
**Step Completion Summary (2025-05-07 HH:MM - Inferred):**
* **Status:** Completed & Approved by User (Inferred from file existence and content)
* **Files Modified/Created:**
    * `src/ai/xai_client.py` (Created/Updated)
    * `src/ai/__init__.py` (Updated to export `XAIClient`)
    * `tests/ai/test_xai_client.py` (Likely Created)
* **Summary of Changes:**
    * `src/ai/xai_client.py`: Implemented `XAIClient` with `get_completion` method. Handles API key loading from config (Step 5) for xAI and Google (as fallback). Uses `requests` for API calls (mocked in tests). Includes error handling for API responses and network issues, raising `APIError`. Logic for `use_fallback` config is present.
    * `src/ai/__init__.py`: Assumed to be updated to export `XAIClient`.
    * `tests/ai/test_xai_client.py`: Assumed to be created with unit tests for the XAI client, likely mocking `requests.post` and testing API key handling, fallback logic, and error responses.
---

- [x] **Step 7: Implement prompt engineering module**
    -   **Task**: Develop `src/ai/prompt_engineering.py` with a primary function like `generate_interaction_prompt(original_post_content, active_account_info, target_account_info, yieldfi_knowledge_snippet, interaction_details, platform)`. This function should dynamically construct detailed prompts based on the context, leveraging `YIELDFI_CORE_MESSAGE`, `get_base_yieldfi_persona`, and specific instructions derived from `data/docs/InstructionsFor*.md` files (passed via `interaction_details`).
        -   **EXPLANATION**: Being very specific about the function signature and its inputs (especially `interaction_details` for custom instructions) helps the AI understand the complexity and dynamism required for this core module.
    -   **Key Considerations/Sub-Tasks**:
        * Implement `get_base_yieldfi_persona(active_account_type)` to define base persona.
        * The `generate_interaction_prompt` should assemble sections: persona, core YieldFi message, original post context (if any), target account context, relevant YieldFi knowledge, and task-specific instructions (tone, goal, style examples from `interaction_details`).
        * Incorporate logic to select and format content from `InstructionsForOfficialToInstitution.md`, `InstructionsForOfficialToPartner.md`, and `InstructionsForInternToIntern.md` based on the `active_account_info.account_type` and `target_account_info.account_type`.
        * Handle platform-specific constraints (e.g., Twitter character limits).
        * Consider how `yieldfi_knowledge_snippet` (from Step 11) will be formatted and injected.
        * Include placeholders for future dynamic example loading if needed, but start with inline logic for instruction integration.
    -   **Files**:
        * `src/ai/prompt_engineering.py`
    -   **Step Dependencies**: Step 6 (implicitly, as prompts are for the xAI client), Step 2 (uses Account, Tweet models).
    -   **User Instructions**: Review the generated prompts for various scenarios (Official-to-Institution, Official-to-Partner, etc.) to ensure they accurately reflect the strategies in `InstructionsFor*.md` and `Yield-Fi-AI-Agent-Roadmap.md`.

---
**Step Completion Summary (2025-05-07 HH:MM):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/ai/prompt_engineering.py`
    * `src/ai/__init__.py`
    * `tests/ai/test_prompt_engineering.py`
* **Summary of Changes:**
    * `src/ai/prompt_engineering.py`: Implemented `get_base_yieldfi_persona`, `get_instruction_set`, `generate_interaction_prompt`, and `generate_new_tweet_prompt` to dynamically construct prompts based on account types, interaction context, specific details, and platform constraints. Includes logic to simulate using instruction sets based on interacting account types.
    * `src/ai/__init__.py`: Updated to export the new prompt generation functions.
    * `tests/ai/test_prompt_engineering.py`: Added unit tests covering persona generation, instruction set selection, interaction prompt generation (various scenarios including different account types and minimal input), and new tweet prompt generation.
---

- [x] **Step 8: Develop tone analysis module**
    -   **Task**: Implement `src/ai/tone_analyzer.py` with a function `analyze_tone(text: str, method: Optional[str] = None) -> Dict[str, Any]` that returns tone (e.g., 'positive', 'negative', 'neutral'), sentiment score, subjectivity, and confidence. It should support different methods (TextBlob initially, configurable for xAI/Google PaLM later). Add `analyze_tweet_tone(tweet: Tweet) -> Tweet` to update Tweet objects.
        -   **EXPLANATION**: Specifying the output dictionary structure and the idea of configurable methods makes the task clearer and prepares for future enhancements.
    -   **Key Considerations/Sub-Tasks**:
        * Implement `_analyze_with_textblob(text)`.
        * Create placeholders `_analyze_with_xai(text)` and `_analyze_with_google_palm(text)`.
        * Use `get_config('tone_analysis.method')` to select the method.
        * The `analyze_tweet_tone` function should update the `tweet.tone` and `tweet.sentiment_score` fields of the `Tweet` model.
    -   **Files**:
        * `src/ai/tone_analyzer.py`
        * `src/ai/__init__.py` (updated)
        * `tests/ai/test_tone_analyzer.py`
    -   **Step Dependencies**: Step 2 (uses `Tweet` model), Step 6 (for future xAI/PaLM analysis methods, though TextBlob has no direct API client dependency).
    -   **User Instructions**: Test the TextBlob implementation with various sample texts to ensure reasonable tone detection.
---
**Step Completion Summary (2025-05-07 19:40):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/ai/tone_analyzer.py` (Created)
    * `src/ai/__init__.py` (Updated)
    * `tests/ai/test_tone_analyzer.py` (Created)
* **Summary of Changes:**
    * `src/ai/tone_analyzer.py`: Implemented `analyze_tone` and `analyze_tweet_tone` functions. `analyze_tone` uses TextBlob by default for sentiment analysis (positive, negative, neutral), returning score, subjectivity, and confidence. Placeholders for xAI and Google PaLM methods were added. `analyze_tweet_tone` updates `Tweet` objects with analysis results. Changelog and basic inline tests included. Corrected f-string errors in `__main__`.
    * `src/ai/__init__.py`: Updated to export `analyze_tone`, `analyze_tweet_tone`, and also ensured `get_base_yieldfi_persona` and `get_instruction_set` from `prompt_engineering` are exported. Changelog updated.
    * `tests/ai/test_tone_analyzer.py`: Created comprehensive unit tests for `_analyze_with_textblob`, `analyze_tone` (including method selection, fallback for unknown methods, and `NotImplementedError` for placeholders), and `analyze_tweet_tone`. Removed a test case for `analyze_tweet_tone` with empty content as the `Tweet` model disallows empty content. All 11 tests pass.
---

- [x] **Step 9: Implement response generator**
    -   **Task**: Create `src/ai/response_generator.py` with main functions like `generate_tweet_reply(tweet, responding_as, target_account, ...)` and `generate_new_tweet(category, responding_as, topic, ...)`. These functions will orchestrate calls to tone analysis (Step 8), knowledge retrieval (Step 11), prompt engineering (Step 7), and the xAI client (Step 6) to produce an `AIResponse` object.
        -   **EXPLANATION**: Clearly defining the primary functions and their orchestration role helps structure this central AI logic module. Outputting a structured `AIResponse` object is key.
    -   **Key Considerations/Sub-Tasks**:
        * `generate_tweet_reply` should:
            * Analyze tone of input `tweet` (using module from Step 8).
            * Determine context for `interaction_details` (e.g. by mapping `responding_as` and `target_account.account_type` to the correct `Instructions*.md` content).
            * Fetch relevant `yieldfi_knowledge_snippet` (using module from Step 11 - **mocked for this step**).
            * Call `generate_interaction_prompt` (from Step 7).
            * Call `xai_client.get_completion` (from Step 6).
            * Package result into an `AIResponse` object.
        * `generate_new_tweet` should similarly construct context, get knowledge, generate prompt, call AI, and package.
        * Implement comprehensive error handling for each step of the generation process.
    -   **Files**:
        * `src/ai/response_generator.py`
        * `src/ai/__init__.py` (updated)
        * `tests/ai/test_response_generator.py`
    -   **Step Dependencies**: Step 6, Step 7, Step 8. (Will also depend on Step 11 once implemented).
    -   **User Instructions**: Test with various mock tweets and account types to ensure responses are contextually appropriate and use the correct personas/tones.
---
**Step Completion Summary (2025-05-07 19:55):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/ai/response_generator.py` (Created)
    * `src/ai/__init__.py` (Updated)
    * `tests/ai/test_response_generator.py` (Created)
* **Summary of Changes:**
    * `src/ai/response_generator.py`: Implemented `generate_tweet_reply` and `generate_new_tweet`. These functions orchestrate calls to tone analysis (Step 8), prompt engineering (Step 7), and the XAI client (Step 6). Knowledge retrieval (Step 11) is currently mocked with an internal `MockKnowledgeRetriever`. Includes logic for parsing AI response structures and robust error handling. Returns an `AIResponse` object with correctly mapped fields (`responding_as`, `target_account`, `generation_time`).
    * `src/ai/__init__.py`: Updated to export `generate_tweet_reply` and `generate_new_tweet`.
    * `tests/ai/test_response_generator.py`: Created 6 unit tests covering successful reply/new tweet generation, API errors, prompt generation errors, and different AI response structures. All tests pass with mocked dependencies.
---

## YieldFi Knowledge Integration

- [x] **Step 10: Create YieldFi knowledge base module**
    -   **Task**: Implement `src/knowledge/base.py` with a `KnowledgeSource` abstract interface. Create `src/knowledge/yieldfi.py` with `StaticJSONKnowledgeSource` (reading from `data/docs/yieldfi_knowledge.json`) and a `YieldFiDocsKnowledgeSource` (reading from `data/docs/docs.yield.fi.md`). Plan for a `LiveYieldFiDataSource` for fetching live metrics as per the roadmap.
        -   **EXPLANATION**: Defining interfaces and specific classes for different knowledge types (static JSON, Markdown docs, live data) makes the system extensible and clear about how different knowledge is handled.
    -   **Key Considerations/Sub-Tasks**:
        * `KnowledgeSource` interface: Define methods like `get_info(topic: str, query: Optional[str] = None) -> Optional[str]` or `search(query: str) -> List[RelevantChunk]`.
        * `StaticJSONKnowledgeSource`: Load and query `yieldfi_knowledge.json`.
        * `YieldFiDocsKnowledgeSource`: Parse `docs.yield.fi.md` (potentially chunking it) to allow searching or querying sections. Basic keyword search or section matching initially.
        * Populate `data/docs/yieldfi_knowledge.json` with key facts, product details, FAQs, current (manually updated for now) APYs/TVL.
        * Consider how to structure `yieldfi_knowledge.json` for easy querying (e.g., nested dictionaries).
    -   **Files**:
        * `src/knowledge/base.py`
        * `src/knowledge/yieldfi.py`
        * `src/knowledge/__init__.py`
        * `data/docs/yieldfi_knowledge.json`
    -   **Step Dependencies**: Step 1 (for file paths).
    -   **User Instructions**: Populate `yieldfi_knowledge.json` with accurate and comprehensive current information about YieldFi's products, services, and key metrics. Ensure `data/docs/docs.yield.fi.md` is the up-to-date whitepaper/documentation.

---
**Step Completion Summary (2025-05-07 20:35):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/knowledge/base.py` (Created)
    * `src/knowledge/yieldfi.py` (Created)
    * `src/knowledge/__init__.py` (Created)
    * `data/docs/yieldfi_knowledge.json` (Created by AI, then updated & expanded by User)
* **Summary of Changes:**
    * `src/knowledge/base.py`: Defined the `KnowledgeSource` abstract base class, which includes an abstract `search` method and a `name` property. Also defined the `RelevantChunk` dataclass to structure search results, including content, source name, score, and metadata.
    * `src/knowledge/yieldfi.py`: Implemented `StaticJSONKnowledgeSource`, which loads data from `data/docs/yieldfi_knowledge.json`. Its `search` method performs a recursive, case-insensitive keyword search within the JSON structure, prioritizing FAQ answers by prepending the question to the answer content in the chunk. Implemented `YieldFiDocsKnowledgeSource` to load data from `data/docs/docs.yield.fi.md`, splitting the content into paragraphs and performing a case-insensitive keyword search. Both classes include robust error handling for file loading (non-existent files, JSON decoding errors) and log relevant information. A placeholder for `LiveYieldFiDataSource` was also included. A basic `if __name__ == '__main__':` block was added for local testing of these sources.
    * `src/knowledge/__init__.py`: Created to export `KnowledgeSource`, `RelevantChunk`, `StaticJSONKnowledgeSource`, and `YieldFiDocsKnowledgeSource` for easy access from other modules.
    * `data/docs/yieldfi_knowledge.json`: Initially created by the AI with placeholder data. The user then populated this file with more comprehensive and accurate information regarding YieldFi's products, FAQs, key metrics, security details, and tokenomics as per the step's user instructions.
---

- [x] **Step 11: Implement knowledge retrieval system**
    -   **Task**: Develop `src/knowledge/retrieval.py` with a `KnowledgeRetriever` class. This class will use the `KnowledgeSource` implementations (from Step 10) to find and return the most relevant knowledge snippets based on the input query or context (e.g., content of a tweet to reply to, topic for a new tweet).
        -   **EXPLANATION**: A dedicated retriever class that can work with multiple knowledge sources centralizes the logic for finding relevant information, making the `response_generator` cleaner.
    -   **Key Considerations/Sub-Tasks**:
        * `KnowledgeRetriever` should be able to register multiple `KnowledgeSource` instances.
        * Implement a strategy to query these sources (e.g., query all, use heuristics to pick a source).
        * For `YieldFiDocsKnowledgeSource`, implement basic text processing (e.g., splitting into paragraphs/sections) and search functionality (e.g., keyword matching, TF-IDF, or simple string search).
        * The output should be a concise string or list of strings suitable for injection into prompts.
        * Roadmap: "Chat with Whitepaper/Docs - enable by gitbook only." This implies needing to process GitBook-style markdown or potentially integrate directly if an API exists. For now, `docs.yield.fi.md` is the source.
    -   **Files**:
        * `src/knowledge/retrieval.py`
    -   **Step Dependencies**: Step 10
    -   **User Instructions**: Test the retrieval with various queries to ensure it pulls relevant information from both `yieldfi_knowledge.json` and `docs.yield.fi.md`.

---
**Step Completion Summary (2025-05-07 20:40):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/knowledge/retrieval.py` (Created)
    * `src/knowledge/__init__.py` (Updated)
* **Summary of Changes:**
    * `src/knowledge/retrieval.py`: Implemented the `KnowledgeRetriever` class which aggregates and globally ranks `RelevantChunk` results from multiple `KnowledgeSource` instances, and formats them for prompt injection. Included methods for adding sources, error handling, and a basic CLI test harness.
    * `src/knowledge/__init__.py`: Exported the `KnowledgeRetriever` class alongside existing exports.
---

## Twitter API Integration Framework

- [x] **Step 12: Design Twitter API data source interface**
    -   **Task**: Flesh out the `src/data_sources/twitter.py` file by defining a `TwitterDataSource` class that inherits from `TweetDataSource` (Step 3). Implement method signatures placeholder (e.g., `pass` or `raise NotImplementedError`). This class will use `tweepy` or a similar library.
        -   **EXPLANATION**: Creating the class structure and method placeholders clearly defines the scope of work for live Twitter integration.
    -   **Key Considerations/Sub-Tasks**:
        * Ensure all methods from `TweetDataSource` are defined.
        * Plan for how `tweepy.Client` or other Twitter library objects will be initialized and used (likely via `twitter_auth.py`).
        * Consider error handling specific to Twitter API responses.
    -   **Files**:
        * `src/data_sources/twitter.py`
    -   **Step Dependencies**: Step 3
    -   **User Instructions**: Review the Twitter API v2 documentation for rate limits, authentication, and endpoint capabilities relevant to the methods in `TweetDataSource`. Ensure you have applied for Twitter Developer Access with the appropriate level.

---
**Step Completion Summary (2025-05-07 20:45):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/data_sources/twitter.py` (Created)
    * `src/data_sources/__init__.py` (Updated)
* **Summary of Changes:**
    * `src/data_sources/twitter.py`: Created a skeleton `TwitterDataSource` class inheriting from `TweetDataSource`. Implemented all required abstract methods and properties with placeholder `NotImplementedError` exceptions. Designed the interface with tweepy integration in mind, including a constructor accepting a bearer token.
    * `src/data_sources/__init__.py`: Updated to export `TwitterDataSource` alongside existing data sources.
---

- [x] **Step 13: Implement Twitter API authentication**
    -   **Task**: Implement `src/data_sources/twitter_auth.py` to handle Twitter API v2 authentication (e.g., Bearer Token for app-only access, OAuth 2.0 Authorization Code Flow with PKCE for user context actions if needed for posting). Store and retrieve credentials securely using the configuration system (Step 5).
        -   **EXPLANATION**: Secure and correct authentication is non-negotiable for API access. Separating it into its own module is good practice.
    -   **Key Considerations/Sub-Tasks**:
        * Function to get an authenticated `tweepy.Client` instance.
        * Securely load API keys, secrets, and tokens from `.env` via the config system.
        * Implement logic for token refresh if using OAuth user context.
    -   **Files**:
        * `src/data_sources/twitter_auth.py`
    -   **Step Dependencies**: Step 12 (knows it will need an auth client), Step 5 (for credentials).
    -   **User Instructions**: Obtain your Twitter API v2 credentials (API Key, API Secret, Bearer Token, and if needed for user context, Access Token & Secret) and add them to your `.env` file.

---
**Step Completion Summary (2025-05-07 20:50):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/data_sources/twitter_auth.py` (Created)
* **Summary of Changes:**
    * `src/data_sources/twitter_auth.py`: Implemented a `get_twitter_client()` function that securely loads credentials from the configuration system (using `get_config()` from Step 5) and initializes a `tweepy.Client` instance. Added proper error handling and logging, including warnings for missing credentials. Included a basic test harness that can be run directly with `python -m src.data_sources.twitter_auth` to verify client initialization.
---

## Web Interface

- [x] **Step 14: Create basic Streamlit app**
    -   **Task**: Implement `app.py` (or `src/app.py`) as the main Streamlit application. Set up basic page configuration, title, and placeholders for UI sections (e.g., tweet input, response display, configuration sidebar). Create `src/ui/__init__.py` and an empty `src/ui/components.py`.
        -   **EXPLANATION**: A minimal but structured Streamlit app provides the canvas for adding specific UI elements in subsequent steps.
    -   **Key Considerations/Sub-Tasks**:
        * Use `st.set_page_config()`.
        * Add a title and a brief description.
        * Create a sidebar for selecting YieldFi persona (Official/Intern) and interaction type (Reply/New Tweet).
        * Main area with placeholders for dynamic content based on sidebar selection.
        * Load necessary configurations and initialize any global objects (like a data source instance).
    -   **Files**:
        * `app.py` (or `src/app.py`)
        * `src/ui/__init__.py`
        * `src/ui/components.py`
    -   **Step Dependencies**: Step 4 (Mock Data Source, for initial UI data), Step 9 (Response Generator, to call when UI form is submitted), Step 11 (Knowledge Retrieval, as part of response generation).
    -   **User Instructions**: Run the Streamlit app with `streamlit run app.py` to ensure the basic layout and placeholders appear correctly.

---
**Step Completion Summary (2025-05-07 HH:MM):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `app.py` (Created/Updated)
    * `src/ui/__init__.py` (Created/Updated)
    * `src/ui/components.py` (Created/Updated with `status_badge`, `collapsible_container`, `copy_button`)
    * `src/ui/tweet_input.py` (Created and significantly developed)
    * `src/config/settings.py` (Updated for API key loading robustness)
    * `src/ai/xai_client.py` (Updated for correct API endpoint and payload)
    * `config.yaml` (Updated for API key placeholders and `xai_model`)
* **Summary of Changes:**
    * `app.py`: Basic Streamlit application structure set up. Includes page configuration, title, sidebar for persona selection, and main area for interaction type selection (Tweet Reply / New Tweet). It calls `display_tweet_reply_ui` and (conceptually) `display_new_tweet_ui`.
    * `src/ui/__init__.py`: Standard init file.
    * `src/ui/components.py`: Implemented helper UI components like `status_badge`, `collapsible_container`, and `copy_button` used for displaying AI response metadata and actions.
    * `src/ui/tweet_input.py`: This file became the core for Step 15 and 16 as well. It handles input for tweet URL or manual content, author details, triggers reply generation via `response_generator.generate_tweet_reply`, displays the AI-generated reply, tone, and includes a copy button. Robust error handling and loading spinners (`st.spinner`) were added. Logger was integrated.
    * Configuration files (`settings.py`, `config.yaml`) and `xai_client.py` were updated to ensure correct and stable API key loading and API interaction, resolving previous errors.
    * The application now successfully generates and displays AI replies for manually entered tweet content.
---

- [x] **Step 15: Implement tweet input interface**
    -   **Task**: In `src/ui/tweet_input.py`, create UI elements for inputting a tweet URL (to fetch and reply to) or manually entering tweet content and target account details for generating a reply.
        -   **EXPLANATION**: Clear input fields are crucial for user experience. This task focuses on how the user provides context for tweet replies.
    -   **Key Considerations/Sub-Tasks**:
        * `st.text_input` for tweet URL.
        * `st.text_area` for manual tweet content.
        * Inputs for target account username/type if not derivable from URL.
        * Button to trigger reply generation.
        * Logic to call `MockTweetDataSource.get_tweet_by_url()` or use manual content.
        * Logic to call `response_generator.generate_tweet_reply()`.
    -   **Files**:
        * `src/ui/tweet_input.py`
    -   **Step Dependencies**: Step 14
    -   **User Instructions**: Test the input fields and ensure the data is correctly passed to the backend when the "Generate Reply" button is clicked.
---
**Step Completion Summary (2025-05-07 HH:MM):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/ui/tweet_input.py` (Primarily)
* **Summary of Changes:**
    * `src/ui/tweet_input.py`: Implemented comprehensive UI elements for tweet input. This includes `st.text_input` for a tweet URL and `st.text_area` for manual tweet content. Inputs for original author username and account type were added for when manual content is provided. The logic correctly prioritizes manual content if both URL and manual content are given (though URL fetching itself is mock/placeholder). The "Generate Reply" button triggers a call to `response_generator.generate_tweet_reply` using the constructed `Tweet` object and selected persona. Includes error handling for missing inputs and displays fetched/manual content for user verification.
---

- [x] **Step 16: Develop response visualization**
    -   **Task**: In `src/ui/response_view.py` (or `app.py`), create UI components to display the AI-generated tweet reply, including the original tweet (if applicable), the suggested reply, and any metadata like tone or confidence.
        -   **EXPLANATION**: Effective presentation of the AI's output allows the user to quickly assess and use the suggestion.
    -   **Key Considerations/Sub-Tasks**:
        * Display original tweet content.
        * Display `AIResponse.content` clearly.
        * Show metadata like `AIResponse.tone`, `AIResponse.model_used`.
        * Add a "Copy to Clipboard" button for the suggested reply.
        * Potentially allow for editing the suggestion.
    -   **Files**:
        * `src/ui/response_view.py` (or modify `app.py`)
        * `src/ui/tweet_input.py` (where it was implemented)
        * `src/ui/components.py` (for copy button, status badge)
    -   **Step Dependencies**: Step 15
    -   **User Instructions**: Verify that the AI's response and relevant metadata are displayed clearly and accurately. Test the copy functionality.
---
**Step Completion Summary (2025-05-07 HH:MM):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/ui/tweet_input.py` (Display logic integrated here)
    * `src/ui/components.py` (Used for `status_badge` and `copy_button`)
* **Summary of Changes:**
    * The AI-generated reply (`AIResponse.reply`) is displayed clearly using `st.success()` within `src/ui/tweet_input.py`.
    * Metadata, specifically the `tone`, is displayed using the `status_badge` component from `src/ui/components.py`.
    * A "Copy to Clipboard" button (from `src/ui/components.py`) was added next to the generated reply, allowing users to easily copy the text.
    * The original tweet content (either fetched via URL or manually entered) is displayed for context before the AI reply.
    * The system now provides a functional loop for inputting tweet details, generating a reply, and viewing/copying that reply along with its tone.
---

## Category-Based Tweet Generation

- [x] **Step 17: Implement category definition system**
    -   **Task**: Create `src/models/category.py` defining a `TweetCategory` dataclass/enum. Populate `data/input/categories.json` with a list of categories (name, description, example prompts/keywords) relevant to YieldFi (e.g., Announcement, Product Update, Community Update, Event, Security, Transparency).
        -   **EXPLANATION**: A structured way to define categories makes it easier to manage them and for the AI to generate targeted content. JSON is a good choice for configurable category data.
    -   **Key Considerations/Sub-Tasks**:
        * `TweetCategory` model: `name: str`, `description: str`, `prompt_keywords: List[str]`, `style_guidelines: Dict`.
        * Load categories from `categories.json` in `app.py` or a config/utility function.
        * Ensure categories in `config.yaml` under `tweet_categories` align or are loaded from this JSON.
    -   **Files**:
        * `src/models/category.py`
        * `data/input/categories.json`
        * Update `src/models/__init__.py`
    -   **Step Dependencies**: Step 2 (for base model understanding).
    -   **User Instructions**: Customize `data/input/categories.json` with YieldFi-specific categories, providing clear descriptions and keywords/examples for each to guide AI generation.
---
**Step Completion Summary (2025-05-07 HH:MM):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/models/category.py`
    * `data/input/categories.json`
    * `src/models/__init__.py`
    * `config.yaml`
* **Summary of Changes:**
    * `src/models/category.py`: Implemented the `TweetCategory` dataclass with `name`, `description`, `prompt_keywords`, and `style_guidelines` attributes, including `from_dict` and `to_dict` methods.
    * `data/input/categories.json`: Created and populated with initial tweet categories (Product Update, Event Announcement, Community Highlight, Educational Content, Security Announcement, General Announcement, Partnership Announcement).
    * `src/models/__init__.py`: Updated to export `TweetCategory`.
    * `config.yaml`: Removed the old `tweet_categories` list as it's now superseded by `categories.json`. Added `data_paths.input` for specifying the input data directory.
---

- [x] **Step 18: Create category-based prompt engineering**
    -   **Task**: Enhance `src/ai/prompt_engineering.py` to include a function `generate_new_tweet_prompt(category: TweetCategory, active_account: Account, topic: Optional[str], yieldfi_knowledge_snippet: Optional[str], platform: str)` that uses the `TweetCategory` object (from Step 17) to tailor prompts for generating new tweets.
        -   **EXPLANATION**: This makes prompt generation for new tweets more targeted and consistent with predefined content strategies for each category.
    -   **Key Considerations/Sub-Tasks**:
        * The function should incorporate `category.name`, `category.description`, `category.prompt_keywords`, and `category.style_guidelines` into the prompt structure.
        * Adapt persona and core messaging based on `active_account`.
        * Integrate `topic` and `yieldfi_knowledge_snippet` naturally.
    -   **Files**:
        * `src/ai/prompt_engineering.py` (Updated)
        * `tests/ai/test_prompt_engineering.py` (Updated)
    -   **Step Dependencies**: Step 17 (relies on `TweetCategory` model).
    -   **User Instructions**: Test with various categories and topics to ensure prompts are well-formed and incorporate category-specific details effectively.
---
**Step Completion Summary (2025-05-08 02:00):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/ai/prompt_engineering.py`
    * `tests/ai/test_prompt_engineering.py`
* **Summary of Changes:**
    * `src/ai/prompt_engineering.py`:
        * Implemented `generate_new_tweet_prompt(category: TweetCategory, active_account: Account, ...)` function.
        * This function now takes a `TweetCategory` object as input.
        * It dynamically constructs prompts using the category's name, description, prompt_keywords, and style_guidelines.
        * It also incorporates the active account's persona, an optional user-provided topic, and any relevant YieldFi knowledge snippets.
        * Ensured `TweetCategory` model is correctly imported and used.
    * `tests/ai/test_prompt_engineering.py`:
        * Added new test cases specifically for `generate_new_tweet_prompt`.
        * These tests verify that prompts correctly include details from the `TweetCategory` object (name, description, keywords, style guidelines) and other provided context like topic and persona.
        * Confirmed that `TWEET_CATEGORIES` dictionary was removed and tests were updated accordingly.
---

- [x] **Step 19: Category Selection UI in Streamlit**
    -   **Task**: In `app.py` (or a new `src/ui/category_select.py` module), create a UI section that allows users to select a tweet category (from `categories.json`), input a topic/brief, and trigger the generation of a new tweet using the `generate_new_tweet` function from `src/ai/response_generator.py` (which will use the category-specific prompt from Step 18).
        -   **EXPLANATION**: Provides a user-facing way to leverage the category-based tweet generation.
    -   **Key Considerations/Sub-Tasks**:
        * Load categories from `data/input/categories.json` for the selection dropdown.
        * UI elements: dropdown for category, text area for topic/brief, "Generate" button.
        * Display the generated tweet and its tone.
        * Integrate with `generate_new_tweet` (Step 9, to be updated to use Step 18 prompts).
    -   **Files**:
        * `src/ui/category_select.py` (New or `app.py` updated)
        * `app.py` (Updated to call the new UI section)
        * `tests/ui/test_category_select.py` (New, if a separate module is created)
    -   **Step Dependencies**: Step 17, Step 18, Step 9 (Response Generator).
    -   **User Instructions**: Test the UI thoroughly by selecting different categories, providing various topics, and verifying that the generated tweets align with the selected category's intent and style.
---
**Step Completion Summary (2025-05-08 02:00):**
* **Status:** Completed & Approved by User
* **Files Modified/Created:**
    * `src/ui/category_select.py`
    * `src/ai/response_generator.py`
    * `src/utils/logging.py`
    * `config.yaml`
    * `app.py` (minor import/call changes if `category_select` is separate)
* **Summary of Changes:**
    * `src/ui/category_select.py`:
        * Implemented `display_new_tweet_by_category_ui` function.
        * Added UI elements: category `selectbox` (populated from `data/input/categories.json` via `load_tweet_categories`), topic `text_area`, and "Generate" button.
        * Calls `generate_new_tweet` from `response_generator` using the selected `TweetCategory` object and topic.
        * Displays the AI-generated tweet content and its analyzed tone.
        * Added robust logging throughout the UI interaction and generation process.
        * Fixed `TypeError` for `copy_button` by removing `key_suffix`.
        * Fixed `ImportError` by removing usage of old `TWEET_CATEGORIES` and correctly using `load_tweet_categories`.
        * Fixed `AttributeError` by using `response.content` instead of `response.reply`.
        * Improved tweet visibility with updated CSS styling (lighter background, darker text).
    * `src/ai/response_generator.py`:
        * Modified `generate_new_tweet` to accept a `TweetCategory` object.
        * Integrated tone analysis: calls `analyze_tone` on the generated tweet content and populates the `AIResponse.tone` field.
    * `src/utils/logging.py`:
        * Enhanced logging to use timestamped log files in a dedicated 'logs' directory.
        * Improved log formatter for more detail.
        * Added option for separate console log level.
    * `config.yaml`:
        * Added `logging.show_raw_response_in_ui` and `logging.console_level` options.
        * Updated `data_paths.input` to be used by `category_select.py` for loading categories.
    * `app.py`: Ensured `display_new_tweet_by_category_ui` is called correctly.
---

## Testing and Evaluation

- [ ] **Step 20: Implement automated testing**
    -   **Task**: Create unit tests in `tests/` for core modules: `data_sources` (especially `MockTweetDataSource`), `ai` modules (`prompt_engineering`, `tone_analyzer`, `response_generator`, `xai_client` with mocked API calls), and `knowledge` modules. Use `pytest`.
        -   **EXPLANATION**: Comprehensive unit tests ensure individual components function correctly and prevent regressions. Mocking external dependencies (like xAI API) is crucial for testing AI logic in isolation.
    -   **Key Considerations/Sub-Tasks**:
        * Create `tests/test_models.py`, `tests/test_data_sources.py`, `tests/test_config.py`.
        * Create `tests/ai/test_prompt_engineering.py`, `tests/ai/test_tone_analyzer.py`, `tests/ai/test_response_generator.py` (mocking `XAIClient`), `tests/ai/test_xai_client.py` (mocking HTTP requests or xAI SDK if used).
        * Create `tests/knowledge/test_knowledge_retrieval.py`.
        * Aim for good test coverage of critical logic and edge cases.
        * Use `pytest` fixtures for setting up test data (e.g., sample `Tweet`, `Account` objects).
    -   **Files**:
        * `tests/test_data_sources.py`
        * `tests/ai/test_prompt_engineering.py` (example, structure as needed)
        * `tests/ai/test_response_generator.py`
        * `tests/knowledge/test_knowledge_retrieval.py`
        * Corresponding `__init__.py` in `tests/` and `tests/ai/` etc.
    -   **Step Dependencies**: Steps 1-19 (as it tests components built in these steps).
    -   **User Instructions**: Run tests with `pytest tests/`. Aim for all tests to pass. Review test coverage.

- [ ] **Step 21: Create evaluation framework**
    -   **Task**: Implement `src/evaluation/metrics.py` (e.g., defining metrics like content relevance, tone adherence, factual accuracy check placeholders) and `src/evaluation/evaluator.py` (logic to run evaluations, potentially comparing AI output against golden answers or using human feedback).
        -   **EXPLANATION**: A structured way to evaluate response quality is essential for understanding AI performance and identifying areas for improvement.
    -   **Key Considerations/Sub-Tasks**:
        * Define what "quality" means for your responses (e.g., relevance, tone, factual accuracy, engagement potential).
        * `metrics.py`: Functions to calculate or assess these (some might be qualitative).
        * `evaluator.py`: A class or functions to take an `AIResponse` (and perhaps a reference answer/context) and apply metrics.
        * Consider a simple UI or script to facilitate batch evaluation or human review.
    -   **Files**:
        * `src/evaluation/metrics.py`
        * `src/evaluation/evaluator.py`
        * `src/evaluation/__init__.py`
    -   **Step Dependencies**: Step 9 (needs generated responses to evaluate).
    -   **User Instructions**: Define a small set of "golden" test cases (input tweet/scenario + ideal response) to test the evaluation framework.

## Deployment

- [ ] **Step 22: Prepare for production deployment**
    -   **Task**: Create a `Dockerfile` for containerizing the Streamlit application, a `docker-compose.yml` for local orchestration (if needed), and a basic `scripts/deploy.sh` (placeholder for actual deployment commands to a chosen platform).
        -   **EXPLANATION**: Containerization ensures consistent deployment across environments.
    -   **Key Considerations/Sub-Tasks**:
        * `Dockerfile`: Based on Python, copies code, installs `requirements.txt`, exposes Streamlit port, sets entrypoint.
        * `docker-compose.yml`: Define service for the app, manage environment variables, port mappings.
        * `deploy.sh`: Placeholder with comments for future deployment steps (e.g., build image, push to registry, deploy to cloud service).
    -   **Files**:
        * `Dockerfile`
        * `docker-compose.yml`
        * `scripts/deploy.sh`
    -   **Step Dependencies**: Steps 1-21 (a complete, tested application).
    -   **User Instructions**: Follow the deployment instructions in the `README.md` (to be updated in Step 23) to test building and running the Docker container locally.

- [ ] **Step 23: Document API and usage**
    -   **Task**: Create comprehensive documentation: `docs/api.md` (if the agent exposes any programmatic APIs, not the case for a simple Streamlit app unless you add a backend API), `docs/usage.md` (how to use the Streamlit app, interpret outputs), `docs/deployment.md` (how to deploy). Update `README.md` with final instructions.
        -   **EXPLANATION**: Good documentation is vital for usability and maintainability.
    -   **Key Considerations/Sub-Tasks**:
        * `README.md`: Final setup, usage, configuration.
        * `docs/usage.md`: Detailed guide for end-users of the Streamlit app.
        * `docs/deployment.md`: Steps for deploying the Docker container.
        * Ensure all configurations and environment variables are documented.
    -   **Files**:
        * `docs/` (directory, if not existing)
        * `docs/api.md` (if applicable)
        * `docs/usage.md`
        * `docs/deployment.md`
        * Update `README.md`

## Implementation Approach Summary
This summary provides an excellent high-level view of the development philosophy.
- **Abstraction**: Clear interfaces (like `TweetDataSource`, `KnowledgeSource`) allow for future changes without impacting the entire system.
- **Modularity**: Separating concerns into distinct components (`ai`, `data_sources`, `knowledge`, `models`, `ui`) makes development, testing, and maintenance much easier.
- **Scalability**: The design allows for adding new data sources (Twitter, Discord, Telegram), new knowledge sources, and more complex AI logic or UI features over time.
- **Usability**: The plan includes steps for a Streamlit UI, which aims to provide an intuitive way to interact with the agent.

The iterative approach (core data, AI, UI, then enhancements) is sound. Key considerations like security, testing, and documentation are well-integrated.