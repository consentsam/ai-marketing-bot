# Changelog:
# 2025-05-07 12:30 - Step 22 - Create Dockerfile for containerizing Streamlit app.

FROM python:3.13-slim

# Set working directory
WORKDIR /app

# Install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . /app

# Expose Streamlit default port
EXPOSE 8501

# Default command to run the Streamlit app
ENTRYPOINT ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"] 