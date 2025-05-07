# YieldFi AI Agent

## Overview

The YieldFi AI Agent is a sophisticated tool designed to enhance YieldFi's social media presence, primarily on Twitter, by automating and optimizing interactions. It leverages advanced AI (via xAI APIs) to generate context-aware tweet replies, create new content based on predefined categories, and integrate with YieldFi's knowledge base for accurate and relevant communication.

This project aims to streamline social media management, ensure brand consistency, and improve engagement with the community, partners, and institutions.

## Features (Planned/Implemented)

* Context-Aware Twitter Reply Generation:
    * Tailors responses based on active YieldFi account (Official, Intern).
    * Adapts tone and style for different target accounts (Partner, Institution, KOL, Community).
    * Utilizes specific interaction guidelines (from `data/docs/InstructionsFor*.md`).
* New Tweet Creation by Category (e.g., Announcements, Product Updates).
* Integration with YieldFi Knowledge Base (`data/docs/docs.yield.fi.md`, live data sources).
* Tone Analysis of incoming tweets to inform response strategy.
* Mock Data Source for development and testing without live API access.
* Modular architecture for future expansion (e.g., Twitter API integration, other social platforms).
* Streamlit-based UI for interaction and content generation.

## Getting Started

### Prerequisites

* Python 3.9+
* Git
* Access to an XAI API key.
* (Eventually) Twitter API Developer Access & Credentials.

### Installation & Setup

1.  **Clone the repository:**
    ```bash
    git clone <your-repository-url>
    cd LLM-Driven-Marketing-Assistant # Or your new project name
    ```

2.  **Create a virtual environment (recommended):**
    ```bash
    python -m venv venv
    source venv/bin/activate  # On Windows: venv\Scripts\activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    * Copy `.env.template` to a new file named `.env`:
        ```bash
        cp .env.template .env
        ```
    * Edit the `.env` file and add your API keys:
        ```
        XAI_API_KEY=your_xai_api_key_here
        # GOOGLE_API_KEY=your_google_api_key_here # If Google Palm is used as a fallback
        # TWITTER_BEARER_TOKEN=... (and other Twitter keys for when live API is integrated)
        ```

5.  **Review Configuration:**
    * Check `config.yaml` for default settings. These are generally overridden by `.env` or can be adjusted if needed.
    * Populate `data/input/sample_tweets.json` and `data/input/sample_accounts.json` if using the mock data source for initial testing.
    * Ensure `data/docs/yieldfi_knowledge.json` (planned in Step 10) is populated with YieldFi specific information.

### Usage

1.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```
    (Note: `app.py` will be developed according to Step 14 of the implementation plan.)

2.  Access the application in your web browser (usually `http://localhost:8501`).
3.  Follow the on-screen instructions to:
    * Select the active YieldFi account persona (e.g., Official, Intern).
    * Input a tweet URL or content to reply to.
    * Provide context about the target account.
    * Or, select a category and topic to generate a new tweet.

## Project Structure

* `data/docs/`: Contains the core implementation plan, roadmap, YieldFi knowledge, and interaction guidelines.
* `data/input/`: Sample data for mock data sources.
* `src/`: Main source code.
    * `src/ai/`: AI integration (xAI client, prompt engineering, response generation, tone analysis).
    * `src/config/`: Configuration management.
    * `src/data_sources/`: Data source abstractions (mock, future Twitter API).
    * `src/knowledge/`: YieldFi knowledge base integration.
    * `src/models/`: Data models (Tweet, Account, AIResponse).
    * `src/ui/`: Streamlit UI components.
    * `src/utils/`: Common utilities (logging, error handling).
* `app.py`: Entry point for the Streamlit application.
* `config.yaml`: Default application configuration.
* `requirements.txt`: Python dependencies.

## Development

+**Prerequisite:** Make sure you are in the project root directory (where `venv/` resides):

```bash
cd /Users/sattu/Dropbox/ai/LLM-Driven-Marketing-Assistant
```

### Running Tests

Ensure your virtual environment is activated:

```bash
source venv/bin/activate
```

Then run:

```bash
pytest tests/
```

Alternatively, invoke pytest through Python:

```bash
python -m pytest tests/
```

#### Ensuring pytest is in your PATH

If `pytest tests/` still fails with "command not found":

```bash
# Add the venv's bin directory to your PATH
export PATH="$(pwd)/venv/bin:$PATH"
```

Verify that you're using the venv's pytest:

```bash
which pytest
# Expect output similar to /Users/sattu/Dropbox/ai/LLM-Driven-Marketing-Assistant/venv/bin/pytest
```

Now you should be able to run:

```bash
pytest tests/
```

Follow the steps outlined in `data/docs/YieldFi-Ai-Agent-Implementation.md`.
Adhere to the rules defined in `.cursor/rules/project-wide-cursor-rules.mdc`.

## Changelog
*(This section will be updated as per Rule 6 of project-wide-cursor-rules.mdc as features are implemented)*

---
### 2025-05-07
- **Step 4: Implement mock tweet data source**
    - Validated `MockTweetDataSource` in `src/data_sources/mock.py` for loading from local JSON files.
    - Confirmed `data/input/sample_tweets.json` and `data/input/sample_accounts.json` exist.
---
### 2025-05-07
- **Step 3: Implement abstract data source interface**
    - Validated `TweetDataSource` abstract base class in `src/data_sources/base.py`.
    - Ensured `src/data_sources/__init__.py` exports the interface.
---
### 2025-05-07
- **Step 2: Define core data models**
    - Validated and aligned data models (`Account`, `Tweet`, `AIResponse`, and related enums/metadata classes) in `src/models/` with the implementation plan.
    - Ensured `from_dict`/`to_dict` methods and docstrings are present.
    - Updated `src/models/__init__.py` to expose all models.
---
### 2025-05-07
- **Step 1: Set up project structure and environment**
    - Created initial directory structure (`src`, `data`, `tests`, etc.).
    - Established `.gitignore` and `requirements.txt`.
    - Created `__init__.py` files for Python package structure.
    - Instructed user on manual creation of `.env.example`.
---