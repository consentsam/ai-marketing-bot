YieldFi AI Agent Usage Guide

This document explains how to use the Ethena (YieldFi) AI Agent Streamlit application once deployed.

⸻

## Running Locally
1. Install Dependencies:
   ```bash
   pip install -r requirements.txt
   ```

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
   
   By default, it will launch on http://localhost:8501.

⸻

## Using the Application

### 1. Sidebar Configuration
- **Account Persona**: Select the YieldFi account persona to respond as (Official or Intern).
- **Interaction Mode**: Select your preferred interaction style (Default, Professional, Degen).
- **Category Selection**: Select the tweet category for generating new tweets (e.g., Announcement, Product Update, Event).

### 2. Interaction Types

#### Generate Tweet Reply
1. Enter a Tweet URL or paste tweet content manually.
2. If entering content manually, provide the original author's username and account type.
3. Check "Generate Poster Image" to create a visual for your tweet.
4. Click "Generate Reply." The AI will produce a context-aware response and an image if requested.
5. Review the generated reply and copy it using the "Copy" button.
6. If an image was generated, it will be displayed below the reply text with its own copy button for the URL.

#### Create New Tweet by Category
1. Select a category from the dropdown menu (Announcement, Product Update, etc.).
2. View category details by expanding the "Category Details & Guidelines" section.
3. Enter a topic or key message in the text area.
4. Check "Generate Poster Image" if you want a visual to accompany your tweet.
5. Click "Generate New Tweet."
6. Review the generated tweet and copy it using the "Copy" button.
7. If an image was generated, it will be displayed below with its URL.

### 3. Additional Features

- **Copy to Clipboard**: Each AI output has a "Copy" button for quick copying.
- **Debug Information**: Expand the "Debug Information" section to see details about the generation process, including the model used, generation time, and prompt.
- **Tone Analysis**: The system analyzes tweet sentiment to shape replies. The tone is displayed above the generated reply.

⸻

## Additional Features

- **Tone Analysis**: The system can internally analyze tweet sentiment to shape replies.
- **Knowledge Retrieval**: If integrated with Ethena knowledge files, it can pull data from yieldfi_knowledge.json or docs.
- **Mock vs. Live Data**: By default, it uses MockTweetDataSource with sample tweets. Switching to live Twitter integration requires implementing TwitterDataSource and setting data_source.type to "twitter" in config.yaml.
- **Image Generation**: Generate compelling visual content for tweets using the Grok image generation API.
- **Protocol Selection**: Use the DEFAULT_PROTOCOL environment variable to switch between different protocol configurations.

⸻

## Troubleshooting

- **No Output or Errors**: Check your console logs or run `streamlit run src/app.py --logger.level=debug`.
- **API Key Issues**: Verify environment variables (XAI_API_KEY, GROK_IMAGE_API_KEY, etc.) are properly loaded (config.yaml or .env).
- **Image Generation Fails**: If the "Generate Poster Image" feature doesn't work, ensure your GROK_IMAGE_API_KEY is valid. A placeholder image will be shown if there's an issue.
- **Deployment**: See docs/deployment.md for details on Vercel deployment. Check logs in your Vercel dashboard if you see blank pages or 500 errors.

⸻

Next Steps
   •  Customize categories in data/input/categories.json.
   •  Expand or refine instruction sets in data/docs/InstructionsFor*.md.
   •  Possibly add "Image Generation" or "Interaction Modes" if continuing the plan from the Implementation steps.
   •  The "Image Generation" feature (Step 24) using GROK_IMAGE_API_KEY is now implemented.
