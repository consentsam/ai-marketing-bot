# Usage Guide

## Local Setup

1. Clone the repository:
   ```bash
   git clone <REPO_URL>
   cd LLM-Driven-Marketing-Assistant
   ```

2. Create and activate a Python virtual environment:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Copy example environment variables and configure:
   ```bash
   cp .env.example .env
   # Edit .env to add your API keys (XAI_API_KEY, GOOGLE_API_KEY, etc.)
   ```

## Running the Application Locally

```bash
streamlit run app.py
```

- Open your browser at `http://localhost:8501`.
- Use the sidebar to select persona and interaction type.
- Input a tweet URL or manual content to generate replies.
- Select a category and topic to generate new tweets.

## Using the YieldFi AI Agent

### Twitter Reply Generation

1. Select "Generate Tweet Reply" from the main interface.
2. Choose your responding persona (Official or Intern) in the sidebar.
3. Either:
   - Enter a tweet URL to fetch and reply to (when integrated with Twitter API)
   - Manually enter tweet content, author information, and account type
4. Click "Generate Reply" to create an AI-powered response.
5. View the generated reply along with its tone analysis.
6. Use the "Copy to Clipboard" button to copy the reply text.

### Category-Based Tweet Generation

1. Select "Create New Tweet by Category" from the main interface.
2. Choose your publishing persona (Official or Intern) in the sidebar.
3. Select a tweet category from the dropdown menu (e.g., Announcement, Product Update).
4. Review the category description, keywords, and style guidelines in the expandable section.
5. Enter your topic or key points in the text area.
6. Click "Generate New Tweet" to create category-specific content.
7. View the generated tweet and use the "Copy Tweet Text" button as needed.

Each category has specific style guidelines and keyword references that help the AI generate appropriate content. The system also incorporates YieldFi knowledge relevant to your selected topic.

## Running Tests

```bash
pytest tests/
```

All critical modules (models, data sources, AI logic, knowledge, evaluation, UI) have unit tests in the `tests/` directory.

## Docker (Optional)

Build and run the Docker container:

```bash
docker build -t yieldfi-ai-agent .
docker run -d --name yieldfi-ai-agent -p 8501:8501 --env-file .env yieldfi-ai-agent:latest
```

## Vercel Deployment

To deploy on Vercel:

1. Ensure you have a `vercel.json` file at the project root:
   ```json
   {
     "version": 2,
     "builds": [
       { "src": "Dockerfile", "use": "@vercel/docker" }
     ],
     "routes": [
       { "src": "/(.*)", "dest": "app.py" }
     ]
   }
   ```

2. Push your repository to GitHub.
3. In the Vercel dashboard, click **Import Project** and select your GitHub repo.
4. Under **Environment Variables**, add the same keys as in your local `.env` (e.g., `XAI_API_KEY`).
5. Deploy. Vercel will build using your Dockerfile and serve the application. 