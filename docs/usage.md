Ethena AI Agent Usage Guide

This document explains how to use the Ethena (YieldFi) AI Agent Streamlit application once deployed.

⸻

Running Locally
   1. Install Dependencies:

pip install -r requirements.txt


   2. Set up environment variables in .env (or however your config expects):

XAI_API_KEY=your_xai_api_key
TWITTER_BEARER_TOKEN=your_twitter_token
... etc ...


   3. Run the app:

streamlit run src/app.py

   •  By default, it will launch on http://localhost:8501.

⸻

Using the Application
   1. Sidebar Configuration: Choose which account persona to respond as (Official or Intern).
   2. Interaction Type:
   •  Generate Tweet Reply:
   •  Provide a Tweet URL or paste tweet content manually.
   •  Click “Generate Reply.” The AI will produce a context-aware response.
   •  Create New Tweet by Category:
   •  Select a category (Announcement, Product Update, etc.).
   •  Enter a topic or key message.
   •  Click “Generate New Tweet.”
   3. Copy to Clipboard: Each AI output has a “Copy” button for quick copying.

⸻

Additional Features
   •  Tone Analysis: The system can internally analyze tweet sentiment to shape replies.
   •  Knowledge Retrieval: If integrated with Ethena knowledge files, it can pull data from yieldfi_knowledge.json or docs.
   •  Mock vs. Live Data: By default, it uses MockTweetDataSource with sample tweets. Switching to live Twitter integration requires implementing TwitterDataSource and setting data_source.type to "twitter" in config.yaml.

⸻

Troubleshooting
   •  No Output or Errors: Check your console logs or run streamlit run src/app.py --logger.level=debug.
   •  API Key Issues: Verify environment variables (XAI_API_KEY, etc.) are properly loaded (config.yaml or .env).
   •  Deployment: See docs/deployment.md for details on Vercel deployment. Check logs in your Vercel dashboard if you see blank pages or 500 errors.

⸻

Next Steps
   •  Customize categories in data/input/categories.json.
   •  Expand or refine instruction sets in data/docs/InstructionsFor*.md.
   •  Possibly add “Image Generation” or “Interaction Modes” if continuing the plan from the Implementation steps.
