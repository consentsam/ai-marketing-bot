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