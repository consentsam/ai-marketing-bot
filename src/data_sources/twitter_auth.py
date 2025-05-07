# Changelog:
# 2025-05-07 20:50 - Step 13.1 - Implemented Twitter API authentication using tweepy and config system.

import logging
from typing import Optional

import tweepy

from src.config.settings import get_config

logger = logging.getLogger(__name__)

def get_twitter_client() -> tweepy.Client:
    """
    Returns an authenticated tweepy.Client instance using credentials from configuration.

    Expects the following keys in config (dot notation):
      - twitter.bearer_token
      - twitter.api_key
      - twitter.api_secret
      - twitter.access_token
      - twitter.access_token_secret

    Raises:
        RuntimeError: If the client cannot be initialized.
    """
    # Load credentials from config
    bearer_token = get_config('twitter.bearer_token')
    api_key = get_config('twitter.api_key')
    api_secret = get_config('twitter.api_secret')
    access_token = get_config('twitter.access_token')
    access_token_secret = get_config('twitter.access_token_secret')

    if not bearer_token:
        logger.warning('TWITTER_BEARER_TOKEN not found in config; GET-only endpoints may fail.')

    try:
        client = tweepy.Client(
            bearer_token=bearer_token,
            consumer_key=api_key,
            consumer_secret=api_secret,
            access_token=access_token,
            access_token_secret=access_token_secret,
            wait_on_rate_limit=True
        )
        logger.info('Twitter Client initialized successfully')
        return client
    except Exception as e:
        logger.error(f'Error initializing Twitter Client: {e}', exc_info=True)
        raise RuntimeError('Failed to create Twitter client') from e

if __name__ == '__main__':
    # Basic test of authentication
    logging.basicConfig(level=logging.INFO)
    try:
        client = get_twitter_client()
        print(f"Twitter client: {client}")
    except Exception as err:
        print(f"Authentication test failed: {err}") 