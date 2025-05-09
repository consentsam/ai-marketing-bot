# YieldFi AI Agent Deployment Guide

This document explains how to deploy the YieldFi AI Agent to Vercel, which replaces the original Docker-based approach. Vercel is a serverless platform that can run Python applications using the @vercel/python builder.

## Why Vercel over Docker?

We've migrated from a Docker-based deployment to Vercel for several key benefits:

1. **Simplified Deployment**: No need to manage containers, volumes, or Docker Compose configurations.
2. **Serverless Architecture**: Scales automatically based on usage without manual management.
3. **Cost Efficiency**: Pay only for the compute you use rather than running a container continuously.
4. **Integrated CI/CD**: Automatic deployments when changes are pushed to your repository.
5. **Built-in SSL/TLS**: Secure HTTPS endpoints provided automatically.

The Docker files (`Dockerfile` and `docker-compose.yml`) remain in the repository for reference but are no longer part of the active deployment workflow.

## Prerequisites

1. **Vercel Account**: Sign up at [vercel.com](https://vercel.com) if you don't have one.
2. **Project Setup**:
    - The repository should contain:
        - A `requirements.txt` listing Python dependencies.
        - A `vercel.json` describing Vercel build rules.
        - A `scripts/start.sh` for launching the Streamlit app.
        - Your main Streamlit file is `app.py` in this project's structure.
3. **Environment Variables**:
    - Required environment variables (API keys, configuration options) should be set in the Vercel project's dashboard under "Settings → Environment Variables".
    - At a minimum, you'll need:
        - `XAI_API_KEY` - Your API key for xAI/Grok.
        - `GROK_IMAGE_API_KEY` - API key for image generation (can be the same as XAI_API_KEY in some cases).
        - `DEFAULT_PROTOCOL` - The default protocol to use (typically "ethena").

## Steps to Deploy

1. **Install Vercel CLI** (optional, for local development):
   ```bash
   npm install -g vercel
   ```

2. **Ensure `vercel.json` exists** in the project root with the following configuration:
   ```json
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
   ```
   This tells Vercel to treat `scripts/start.sh` as our main entry point.

3. **Verify `scripts/start.sh`** contains:
   ```bash
   #!/usr/bin/env bash
   
   # Set default PORT if not provided by Vercel
   if [ -z "$PORT" ]; then
       export PORT=8501
   fi
   
   # Install dependencies quietly
   pip install -r requirements.txt --quiet
   
   # Run Streamlit with minimal output
   echo "Starting Streamlit on port $PORT..."
   streamlit run app.py --server.port "$PORT" --browser.serverAddress "0.0.0.0" --server.enableCORS true --server.enableWebsocketCompression true --server.enableXsrfProtection false
   ```

4. **Make sure `runtime.txt`** specifies a Python version compatible with Vercel:
   ```
   python-3.9
   ```

5. **Push code to Git**:
   ```bash
   git add .
   git commit -m "Add Vercel deployment configs"
   git push origin main
   ```

6. **Import repository into Vercel**:
   - Go to [vercel.com/import](https://vercel.com/import)
   - Select your Git provider (GitHub, GitLab, Bitbucket) and repository
   - Follow the prompts to configure your project

7. **Set environment variables** in the Vercel dashboard:
   - Go to your project settings
   - Navigate to the "Environment Variables" tab
   - Add the required variables (XAI_API_KEY, GROK_IMAGE_API_KEY, DEFAULT_PROTOCOL, etc.)

8. **Trigger a deployment**:
   - Vercel will detect the @vercel/python usage from vercel.json
   - It will install dependencies from requirements.txt
   - Then run scripts/start.sh to start your Streamlit app

9. **Confirm deployment**:
   - Your app will be accessible at `https://[projectname].vercel.app`
   - Check the "Logs" section in Vercel to see any console messages or errors

## Troubleshooting Deployment Issues

- **App loads but shows blank page or errors**: Check Vercel function logs for Python errors or missing dependencies.
- **Function timeout errors**: The default function timeout is 10 seconds. If your app initialization takes longer, increase the timeout in your Vercel project settings under "Settings → Functions → General → Timeout".
- **Missing dependencies**: Ensure all required packages are in `requirements.txt`. Some packages may need to be specified with exact versions to avoid compatibility issues.
- **Environment variables not working**: Verify they are correctly set in the Vercel dashboard, not just in your local `.env` file.
- **PORT issues**: Make sure `start.sh` correctly uses the `$PORT` environment variable provided by Vercel.

## Local Testing with Vercel Dev

You can test your Vercel deployment locally before pushing to production:

1. **Install Vercel CLI** if you haven't already:
   ```bash
   npm install -g vercel
   ```

2. **Link your local project** to your Vercel project:
   ```bash
   vercel link
   ```

3. **Pull environment variables** from your Vercel project:
   ```bash
   vercel env pull
   ```

4. **Run the development server**:
   ```bash
   vercel dev
   ```

This will simulate the Vercel deployment environment locally, allowing you to test your application before deploying.

## Continuous Deployment

Vercel supports continuous deployment from Git. Each push to your main branch will trigger a new deployment. You can also:

- Preview deployments from pull requests
- Set up staging environments with different environment variables
- Configure custom domains for your production deployment

For more details, refer to the [Vercel documentation](https://vercel.com/docs).