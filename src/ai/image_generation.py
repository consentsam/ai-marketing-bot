"""
Image generation module for the YieldFi AI Agent.

This module provides functions to generate poster images based on prompts.

# Changelog:
# 2025-05-09 10:30 - Step 24 - Created image generation module with API key handling.
"""

import logging
import os
from typing import Optional
import requests  # Added for HTTP calls

try:
    from src.config.settings import get_config
except ImportError:
    def get_config(key, default=None):
        return os.environ.get(key, default)

logger = logging.getLogger(__name__)


def get_poster_image(prompt: str) -> str:
    """
    Generates or retrieves a poster image for the given prompt.

    Args:
        prompt: The prompt or text to generate an image for.

    Returns:
        A URL string pointing to the generated image.
    """
    # Get API key from config or environment
    api_key = get_config("grok_image_api_key") or os.environ.get("GROK_IMAGE_API_KEY")
    
    # Log API key availability (without revealing it)
    if api_key:
        logger.info("GROK_IMAGE_API_KEY found, will attempt to use actual image generation API")
    else:
        logger.error("GROK_IMAGE_API_KEY not set in environment or config. Using placeholder image.")
        return "https://placehold.co/512x512?text=No+API+Key"
    
    logger.info(f"Generating poster image for prompt: '{prompt[:100]}...'")
    
    # Prepare request to Grok Image Generation API
    url = "https://api.x.ai/v1/images/generations"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "grok-2-image",
        "prompt": prompt,
        "n": 1,
        "response_format": "url"
    }
    try:
        resp = requests.post(url, headers=headers, json=payload, timeout=30)
        resp.raise_for_status()
        body = resp.json()
        img_url = body.get("data", [])[0].get("url")
        if img_url:
            logger.info(f"Generated image URL: {img_url}")
            return img_url
        else:
            logger.error("No URL field in image generation response, using placeholder.")
    except Exception as e:
        logger.error(f"Image generation failed: {e}", exc_info=True)
    # Fallback placeholder on error
    return "https://placehold.co/512x512?text=Image+Error" 