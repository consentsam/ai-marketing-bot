
Ethena AI Agent Deployment Guide

This document explains how to deploy the Ethena AI Agent (YieldFi AI Assistant) to Vercel, which replaces the original Docker-based approach. Vercel is a serverless platform that can run Python applications using the @vercel/python builder.

⸻

Prerequisites
   1. Vercel Account: Sign up at vercel.com if you don’t have one.
   2. Project Setup:
   •  The repository should contain:
   •  A requirements.txt listing Python dependencies.
   •  A vercel.json describing Vercel build rules.
   •  A scripts/start.sh for launching the Streamlit app.
   •  Your main Streamlit file is src/app.py in this project’s structure.
   3. Environment Variables:
   •  If you need secrets (e.g., XAI_API_KEY, TWITTER_BEARER_TOKEN), set them in the Vercel project’s dashboard under “Settings → Environment Variables.”

⸻

Steps to Deploy
   1. Install Vercel CLI (optional, if you want local dev):

npm install -g vercel


   2. Create vercel.json in the project root (if not already present):

{
  "builds": [
    {
      "src": "scripts/start.sh",
      "use": "@vercel/python"
    }
  ],
  "routes": [
    {
      "src": "/(.*)",
      "dest": "scripts/start.sh"
    }
  ]
}

   •  This tells Vercel to treat scripts/start.sh as our main entry point.

   3. Create/Update scripts/start.sh:

#!/usr/bin/env bash
...
# (See the final version with minimal logs)

   •  This script runs pip install -r requirements.txt quietly and starts Streamlit on $PORT.

   4. Push code to Git:

git add .
git commit -m "Add Vercel deployment configs"
git push origin main


   5. Import repository into Vercel:
   •  Go to vercel.com/import.
   •  Select your Git provider and repository.
   6. Set environment variables in Vercel dashboard, if needed.
   7. Trigger a deploy:
   •  Vercel will detect @vercel/python usage from vercel.json.
   •  Install your dependencies from requirements.txt.
   •  Run scripts/start.sh.
   8. Confirm Deployment:
   •  Your app will be accessible at [projectname].vercel.app.
   •  Check “Logs” in Vercel to see any console messages or errors.

⸻

Logs & Debugging
   •  By default, the updated start.sh runs almost silently. If you encounter errors or test failures:
   •  Check your Vercel “Function Logs” or “Build Logs” for Python tracebacks.
   •  Temporarily add set -x or echo statements to start.sh if you need more verbose output.

⸻

Next Steps
   •  If you want more advanced routing or custom domains, configure them in Vercel’s project settings.
   •  For scaling or concurrency, consider the usage patterns of your AI calls. If the LLM calls are not stateful, it should scale fine on Vercel.

That’s it! You are now fully deployed on Vercel.