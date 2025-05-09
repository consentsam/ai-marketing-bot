YieldFi AI Agent Usage Guide

This document explains how to use the Ethena (YieldFi) AI Agent Streamlit application once deployed.

⸻

Running Locally
   1. Install Dependencies:

pip install -r requirements.txt


   2. Set up environment variables in `.env` (or however your config expects):

      ```bash
XAI_API_KEY=your_xai_api_key
      # GOOGLE_API_KEY=your_google_api_key_here # If PaLM fallback is configured
TWITTER_BEARER_TOKEN=your_twitter_token
      DEFAULT_PROTOCOL=ethena # Default protocol for categories and knowledge
      GROK_IMAGE_API_KEY=your_grok_image_api_key_here # For poster image generation via XAI/Grok (Step 24)
      ```


   3. Run the app:

   ```bash
   streamlit run app.py
   ```

   •  By default, it will launch on http://localhost:8501.

⸻

Using the Application
   1. Sidebar Configuration:
      - Select the YieldFi account persona to respond as (Official or Intern).
      - Select an Interaction Mode (e.g., Default, Professional, Degen).
      - (Optional) Check "Generate Poster Image" under the tweet input area to generate an accompanying image for the response.
      <!-- TODO: Insert screenshot of the tweet input area showing the "Generate Poster Image" checkbox -->
   2. Interaction Type:
   •  Generate Tweet Reply:
   •  Provide a Tweet URL or paste tweet content manually.
   •  Optionally, check "Generate Poster Image" before generating.
   •  Click "Generate Reply." The AI will produce a context-aware response and an image if requested.
   •  Create New Tweet by Category:
   •  Select a category (Announcement, Product Update, etc.).
   •  Enter a topic or key message.
   •  Optionally, check "Generate Poster Image" before generating (if available in this UI section).
   •  Click "Generate New Tweet."
   3. Copy to Clipboard: Each AI output has a "Copy" button for quick copying.
   4. Image Display: If an image is generated, it will be displayed below the tweet text with its own copy button for the URL.

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
   •  Possibly add "Image Generation" or "Interaction Modes" if continuing the plan from the Implementation steps.
   •  The "Image Generation" feature (Step 24) using GROK_IMAGE_API_KEY is now implemented.
