# Changelog:
# 2025-05-07 HH:MM - Step 19 - Initial implementation of category selection UI for new tweet generation.
# 2025-05-07 HH:MM - Bugfix - Use response.content instead of response.reply.
# 2025-05-08 00:45 - User Request - Removed unexpected key_suffix from copy_button call.
# 2025-05-07 23:50 - Step 19.1 - Implemented UI for selecting tweet category, inputting details, and generating tweets.
# 2025-05-08 01:15 - User Request - Fix ImportError for TWEET_CATEGORIES, ensure use of load_tweet_categories.

import streamlit as st
import json
from typing import List, Optional, cast, Dict, Any
import time # For unique keys if needed, though st.session_state is better
from datetime import datetime, timezone
import os # IMPORT OS HERE for os.path.exists

from src.models.category import TweetCategory
from src.models.account import Account, AccountType
from src.models.response import AIResponse
from src.ai.response_generator import generate_new_tweet
# from src.ai.prompt_engineering import TWEET_CATEGORIES # REMOVE THIS LINE - Causes ImportError
from src.ui.components import status_badge, copy_button # Reusing components
from src.utils.logging import get_logger
from src.utils.error_handling import APIError # IMPORT APIError
from src.config.settings import get_config # Added

logger = get_logger(__name__)

DATA_CATEGORIES_PATH = get_config("data_paths.input", "data/input") + "/categories.json" # Use config for path
logger.info(f"Categories JSON path set to: {DATA_CATEGORIES_PATH}")

@st.cache_data(ttl=3600) # Cache for 1 hour to avoid frequent reloads
def load_tweet_categories(file_path: str = DATA_CATEGORIES_PATH) -> List[TweetCategory]:
    """Loads tweet categories from the specified JSON file."""
    logger.info(f"Attempting to load tweet categories from: {file_path}")
    categories: List[TweetCategory] = []
    try:
        if not os.path.exists(file_path):
            logger.error(f"Categories file not found at path: {file_path}")
            st.error(f"Critical Error: Categories definition file not found at {file_path}. Please create it and ensure the path in config.yaml (data_paths.input) is correct.")
            return [] # Return empty list if file not found
        
        with open(file_path, 'r') as f:
            data = json.load(f)
            logger.debug(f"Successfully read data from {file_path}")
            if isinstance(data, list):
                for cat_data in data:
                    if isinstance(cat_data, dict):
                        try:
                            category_obj = TweetCategory.from_dict(cat_data)
                            categories.append(category_obj)
                            logger.debug(f"Successfully parsed category: {category_obj.name}")
                        except Exception as e:
                            logger.error(f"Error parsing category data: {cat_data}. Error: {e}", exc_info=True)
                    else:
                        logger.warning(f"Skipping non-dictionary item in categories data: {cat_data}")
            else:
                logger.error(f"Categories file {file_path} does not contain a list. Found type: {type(data)}")
    except FileNotFoundError: # This is now handled by os.path.exists check above, but keep for safety.
        logger.error(f"Categories file not found (redundant check): {file_path}", exc_info=True)
        st.error(f"Error: Categories definition file not found at {file_path}.")
    except json.JSONDecodeError as e:
        logger.error(f"Error decoding JSON from {file_path}: {e}", exc_info=True)
        st.error(f"Error: Could not parse categories file. Invalid JSON: {e}")
    except Exception as e:
        logger.error(f"An unexpected error occurred loading categories from {file_path}: {e}", exc_info=True)
        st.error(f"An unexpected error occurred while loading tweet categories.")
    
    if not categories:
        logger.warning(f"No categories were loaded from {file_path}.")
    else:
        logger.info(f"Successfully loaded {len(categories)} categories.")
    return categories

# Helper function to display tone badge (similar to tweet_input.py)
def display_tone_badge(tone: Optional[str], prefix: str = "Tone: "):
    if tone and tone != "N/A":
        # Simplistic mapping, can be expanded
        if "positive" in tone.lower():
            badge_status = "success"
        elif "negative" in tone.lower():
            badge_status = "error"
        elif "neutral" in tone.lower():
            badge_status = "info"
        else:
            badge_status = "info" # Default for unknown
        status_badge(f"{prefix}{tone}", badge_status)
    elif tone == "N/A":
        status_badge(f"{prefix}N/A", "info")

def display_new_tweet_by_category_ui(active_account_type: AccountType):
    """User interface for generating a new tweet based on a selected category."""
    st.subheader("Create New Tweet by Category")
    logger.debug(f"Displaying 'Create New Tweet by Category' UI for account type: {active_account_type.value}")

    categories: List[TweetCategory] = load_tweet_categories()

    if not categories:
        logger.warning("No tweet categories loaded. UI will show a warning.")
        st.warning(f"No tweet categories are defined or could be loaded from '{DATA_CATEGORIES_PATH}'. Please add categories to this file.")
        return

    category_names = [cat.name for cat in categories]
    logger.debug(f"Available category names for selectbox: {category_names}")
    
    selected_category_name = st.selectbox(
        "Select Tweet Category:",
        options=category_names,
        index=0 if category_names else -1, # Handle empty category_names
        key="new_tweet_category_selector"
    )
    logger.debug(f"Selected tweet category name from selectbox: {selected_category_name}")

    selected_category_obj: Optional[TweetCategory] = None
    if selected_category_name:
        # Find the selected TweetCategory object
        for cat in categories:
            if cat.name == selected_category_name:
                selected_category_obj = cat
                break
    
    if selected_category_obj:
        logger.debug(f"Found matching TweetCategory object for '{selected_category_name}': {selected_category_obj}")
        st.markdown(f"**Description:** {selected_category_obj.description}")
        if selected_category_obj.prompt_keywords: # Check if list is not empty
             st.markdown(f"**Keywords:** `{', '.join(selected_category_obj.prompt_keywords)}`")
        else:
            st.markdown("**Keywords:** `N/A`")

        # Collapsible Style Guidelines
        if selected_category_obj.style_guidelines: # Check if dict is not empty
            with st.expander("View Style Guidelines"):
                for k, v in selected_category_obj.style_guidelines.items():
                    st.markdown(f"- **{k.capitalize()}**: {v}")
                logger.debug(f"Displaying style guidelines for {selected_category_name}")
        else:
            with st.expander("View Style Guidelines", expanded=False):
                st.markdown("No specific style guidelines defined for this category.")
    else:
        logger.warning(f"Could not find a TweetCategory object for selected name: {selected_category_name}, though it was in options. This is unexpected.")
        # This case should ideally not happen if selected_category_name comes from category_names

    topic_key_message = st.text_area(
        "Enter Topic / Key Message / Brief for the tweet:",
        height=150,
        key="new_tweet_topic_input",
        placeholder="E.g., Announce new yUSDPool with 15% APY and $SPENDLE rewards, maturity 90 days."
    )
    logger.debug(f"Topic/Key Message input: '{topic_key_message[:50]}...' (truncated if long)")

    if st.button("Generate Tweet", key="generate_new_tweet_button"):
        logger.info(f"Generate Tweet button clicked for category: {selected_category_name} and persona: {active_account_type.value}")
        # Ensure selected_category_obj is used here instead of selected_category_name where a TweetCategory object is expected
        if not selected_category_obj: # CHECK THIS OBJECT
            st.error("Please select a valid category.")
            logger.error("Tweet generation attempted without a valid selected category object.")
            return
        
        logger.debug(f"User input for tweet generation: Topic='{topic_key_message}', Category Object='{selected_category_obj.name}'")

        if not topic_key_message.strip(): # topic_key_message.strip() is correct
            st.warning("Topic/Brief is empty. The AI will generate based on the category's general theme if possible.")
            # Allow generation even if topic is empty, prompt_engineering should handle it.
            # logger.warning("Tweet generation attempted with empty topic/message.")
            # return # Removing the return to allow generation with empty topic

        # Initialize session state for generated content if not already present
        if "generated_new_tweet_reply" not in st.session_state:
            st.session_state.generated_new_tweet_reply = None
        if "generated_new_tweet_tone" not in st.session_state:
            st.session_state.generated_new_tweet_tone = None
        if "full_new_ai_response" not in st.session_state:
            st.session_state.full_new_ai_response = None
        
        logger.debug("Session state initialized/checked for new tweet generation.")

        with st.spinner("Generating new tweet..."):
            try:
                logger.debug(f"Calling generate_new_tweet with category object='{selected_category_obj.name}', topic='{topic_key_message[:50]}...', persona='{active_account_type.value}'")
                response: AIResponse = generate_new_tweet(
                    category=selected_category_obj, # PASS THE TweetCategory OBJECT
                    topic=topic_key_message.strip(),
                    responding_as_type=active_account_type,
                )
                logger.info(f"Successfully generated tweet for category: {selected_category_obj.name}")
                # Log the received AIResponse content and full details
                logger.debug(f"AIResponse received: Content='{response.content[:50]}...', Tone='{response.tone}', FullResponse: {response.to_dict()}" )

                # Store the generated content in session state
                st.session_state.generated_new_tweet_reply = response.content
                st.session_state.generated_new_tweet_tone = response.tone if response.tone else "N/A"
                st.session_state.full_new_ai_response = response # Store the full response
                logger.debug("Stored generated tweet, tone, and full response in session state.")

            except APIError as e:
                st.error(f"Error generating tweet: {e}")
                logger.error(f"APIError during tweet generation for category {selected_category_obj.name}: {e}", exc_info=True)
                st.session_state.generated_new_tweet_reply = f"Error: AI API failed. ({e})"
                st.session_state.generated_new_tweet_tone = "Error"
            except Exception as e:
                st.error(f"An unexpected error occurred: {e}")
                logger.error(f"Unexpected error during tweet generation for category {selected_category_obj.name}: {e}", exc_info=True)
                st.session_state.generated_new_tweet_reply = f"Error: An unexpected issue occurred. ({e})"
                st.session_state.generated_new_tweet_tone = "Error"
        
        # Display generated tweet if available in session state
        if "generated_new_tweet_reply" in st.session_state and st.session_state.generated_new_tweet_reply:
            logger.debug(f"Displaying generated tweet from session state: '{st.session_state.generated_new_tweet_reply[:50]}...'")
            st.subheader("AI-Generated Tweet:")
            st.markdown(
                f'''
                <div style="border: 1px solid #cccccc; padding: 15px; border-radius: 5px; background-color: #f9f9f9; color: #333333; font-size: 1.1em; line-height: 1.6;">
                    {st.session_state.generated_new_tweet_reply}
                </div>
                ''',
                unsafe_allow_html=True,
            )
            
            # Display tone badge
            logger.debug(f"Displaying tone badge for tone: {st.session_state.generated_new_tweet_tone}")
            display_tone_badge(st.session_state.generated_new_tweet_tone, prefix="AI Suggested Tone: ")

            # Add a copy button
            if st.session_state.generated_new_tweet_reply and "Error:" not in st.session_state.generated_new_tweet_reply :
                logger.debug("Adding copy button for the generated tweet.")
                copy_button(st.session_state.generated_new_tweet_reply) 
            else:
                logger.debug("Not adding copy button due to error in generated reply or empty reply.")

            # Display full response for debugging if enabled in config
            if get_config("logging.show_raw_response_in_ui", False): # New config option
                with st.expander("View Full AI Response (Debug)"):
                    st.json(st.session_state.full_new_ai_response.to_dict() if st.session_state.full_new_ai_response else {})
                    logger.debug("Displayed full AI response in UI for debugging.")
        else:
            logger.debug("No generated tweet found in session state to display.")

# Basic test harness if run directly (for quick UI checks without full app)
if __name__ == '__main__':
    st.set_page_config(layout="wide", page_title="Test Category Tweet UI")
    # Ensure categories.json has data for this test to be useful
    # Create a dummy categories.json if it doesn't exist for testing
    if not os.path.exists(DATA_CATEGORIES_PATH):
        sample_cat_data_for_direct_run = [
            {
                "name": "Test Category 1",
                "description": "This is a test category for direct UI running.",
                "prompt_keywords": ["test", "example"],
                "style_guidelines": {"tone": "neutral"}
            }
        ]
        with open(DATA_CATEGORIES_PATH, 'w') as f_temp:
            json.dump(sample_cat_data_for_direct_run, f_temp)
        st.info(f"Created temporary {DATA_CATEGORIES_PATH} for direct run testing.")
    
    # Simulate persona selection from app.py sidebar
    test_persona = st.sidebar.selectbox(
        "Respond as (Test Persona):", 
        options=[atype.value for atype in AccountType],
        index=[atype.value for atype in AccountType].index(AccountType.OFFICIAL.value) # Default to Official
    )
    selected_account_type = AccountType(test_persona)

    display_new_tweet_by_category_ui(selected_account_type)

    st.markdown("---")
    st.write("Note: This is a direct run of category_select.py. Full app functionality might differ.")
    st.write("Ensure `data/input/categories.json` exists and is populated for full category options.")

    # Clean up dummy file if created
    # This cleanup logic is tricky with Streamlit's execution model on direct run.
    # Manual cleanup might be needed if you stop the script early.
    # Consider not auto-creating for direct run to avoid complexity. 