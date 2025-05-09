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
    * Select from predefined categories with tailored prompts and style guidelines.
    * Provide topic or key points for content generation.
    * AI adapts to the selected YieldFi persona (Official, Intern).
* Integration with YieldFi Knowledge Base (`data/docs/docs.yield.fi.md`, live data sources).
* Tone Analysis of incoming tweets to inform response strategy.
* Image Generation for tweets with visual content.
* Mock Data Source for development and testing without live API access.
* Modular architecture for future expansion (e.g., Twitter API integration, other social platforms).
* Streamlit-based UI for interaction and content generation.
* Protocol-specific knowledge and configuration (with support for multiple protocols).

## Getting Started

### Prerequisites

* Python 3.9+
* Git
* Access to an XAI API key.
* Grok image API key (for poster image generation).
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
    * Copy `.env.example` to a new file named `.env`:
        ```bash
        cp .env.example .env
        ```
    * Edit the `.env` file and add your API keys:
        ```
        XAI_API_KEY=your_xai_api_key_here
        # GOOGLE_API_KEY=your_google_api_key_here # If Google PaLM is used as a fallback
        # TWITTER_BEARER_TOKEN=... (and other Twitter keys for when live API is integrated)
        DEFAULT_PROTOCOL=ethena # Default protocol for categories and knowledge
        GROK_IMAGE_API_KEY=your_grok_image_api_key_here # For poster image generation via XAI/Grok
        ```

5.  **Review Configuration:**
    * Check `config.yaml` for default settings. These are generally overridden by `.env` or can be adjusted if needed.
    * Populate `data/input/sample_tweets.json` and `data/input/sample_accounts.json` if using the mock data source for initial testing.
    * Ensure `data/docs/yieldfi_knowledge.json` is populated with YieldFi specific information.
    * Customize `data/input/categories.json` with YieldFi-specific tweet categories if using the category-based tweet generation feature.

### Usage

1.  **Run the Streamlit application:**
    ```bash
    streamlit run app.py
    ```

2.  Access the application in your web browser (usually `http://localhost:8501`).
3.  Follow the on-screen instructions to:
    * Select the active YieldFi account persona (e.g., Official, Intern).
    * Choose an interaction type:
        * **Generate Tweet Reply**: Input a tweet URL or content to reply to and provide context about the target account. Optionally check "Generate Poster Image" to create a visual for your reply.
        * **Create New Tweet by Category**: Select a category (e.g., Announcement, Product Update), enter a topic, and generate a tailored new tweet. Optionally check "Generate Poster Image" to include a visual with your tweet.

For detailed usage instructions, see [Usage Guide](docs/usage.md).

## Project Structure

* `data/docs/`: Contains the core implementation plan, roadmap, YieldFi knowledge, and interaction guidelines.
* `data/input/`: Sample data for mock data sources, tweet categories, etc.
* `data/protocols/`: Protocol-specific data, including knowledge, categories, and mode instructions.
* `src/`: Main source code.
    * `src/ai/`: AI integration (xAI client, prompt engineering, response generation, tone analysis, image generation).
    * `src/config/`: Configuration management.
    * `src/data_sources/`: Data source abstractions (mock, future Twitter API).
    * `src/knowledge/`: YieldFi knowledge base integration.
    * `src/models/`: Data models (Tweet, Account, AIResponse, TweetCategory).
    * `src/ui/`: Streamlit UI components.
    * `src/utils/`: Common utilities (logging, error handling).
* `app.py`: Entry point for the Streamlit application.
* `config.yaml`: Default application configuration.
* `requirements.txt`: Python dependencies.
* `vercel.json`: Vercel deployment configuration.
* `runtime.txt`: Python runtime specification for Vercel.

## Development

**Prerequisite:** Make sure you are in the project root directory (where `venv/` resides):

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

## Deployment

The application can be deployed to Vercel. See [Deployment Guide](docs/deployment.md) for detailed instructions.

## Changelog
*(This section will be updated as per Rule 6 of project-wide-cursor-rules.mdc as features are implemented)*

---
### 2025-05-18
- **Step 23: Documentation & Final Updates**: Refreshed README and documentation to reflect new features (environment variables, usage updates); updated `docs/usage.md` and `docs/api.md`. Added detailed docs for image generation feature and Vercel deployment.

---
### 2025-05-09
- **Step 24: Image Generation**: Implemented image generation using XAI/Grok API. Added `GROK_IMAGE_API_KEY` to environment variables. Integrated image generation into the response flow and UI, allowing users to optionally generate and view a poster image alongside tweets.

---
### 2025-05-08
- **Steps 17-19: Category-Based Tweet Generation**
    - Implemented `TweetCategory` model and category definition system.
    - Extended prompt engineering for category-specific tweet generation.
    - Developed UI for category selection, topic input, and tweet generation.
    - Added comprehensive documentation for the category-based features.
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

## Documentation

- **API Reference:** [docs/api.md](docs/api.md)
- **Usage Guide:** [docs/usage.md](docs/usage.md)
- **Deployment Guide:** [docs/deployment.md](docs/deployment.md)