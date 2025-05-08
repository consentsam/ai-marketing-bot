#!/usr/bin/env bash

###############################################################################
# Start script for running Streamlit on Vercel
# Updated to reduce nearly all logs and run silently unless an error occurs.
###############################################################################

# Remove 'set -x' and all verbose logging to keep the script silent.

# Check if PORT is set, or default to 8501
if [ -z "$PORT" ]; then
  export PORT=8501
fi

# Check for the Streamlit app file
if [ ! -f "src/app.py" ]; then
  # Fail silently if missing
  exit 1
fi

# Install dependencies in quiet mode
pip install --upgrade --no-cache-dir -r requirements.txt -q

# Run the Streamlit app
exec streamlit run src/app.py --server.port "$PORT" --server.address 0.0.0.0