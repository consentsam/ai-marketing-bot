# Changelog:
# 2025-05-07 HH:MM - Step 19 - Initial creation of category selection UI.
# 2025-05-07 HH:MM - Bugfix - Use response.content instead of response.reply.
# 2025-05-08 00:45 - User Request - Removed unexpected key_suffix from copy_button call.
# 2025-05-07 23:50 - Step 19.1 - Implemented UI for selecting tweet category, inputting details, and generating tweets.
# 2025-05-08 01:15 - User Request - Fix ImportError for TWEET_CATEGORIES, ensure use of load_tweet_categories.
# 2025-05-08 HH:MM - Bugfix - Remove references to non-existent response.error attribute.

"""
UI for generating new tweets based on categories.

Purpose: Provides the Streamlit UI components for selecting a tweet category,
         inputting a topic, and generating/displaying a new tweet.
Rationale: A dedicated UI module for this functionality keeps app.py cleaner
           and organizes UI code logically.
Usage: Imported and called by app.py when the user selects
       'Create New Tweet by Category'.
"""

import streamlit as st
import json
from typing import List, Optional, cast, Dict, Any
import time # For unique keys if needed, though st.session_state is better
from datetime import datetime, timezone
import os # IMPORT OS HERE for os.path.exists

from src.models.category import TweetCategory, load_categories
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

# Load categories once when the module is loaded
# This makes them available for the UI without reloading on every interaction
# if the list of categories is static during the app's runtime.
AVAILABLE_CATEGORIES: List[TweetCategory] = load_categories()

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

def display_category_tweet_ui(active_account_type: AccountType):
    """Displays UI for creating a new tweet by category."""
    logger.info(f"Displaying category tweet UI for persona: {active_account_type.value}")
    st.subheader("Create New Tweet by Category")

    if not AVAILABLE_CATEGORIES:
        st.error("No tweet categories are available. Please check the category definitions.")
        logger.error("display_category_tweet_ui: No categories loaded from load_categories().")
        return

    category_names = [cat.name for cat in AVAILABLE_CATEGORIES]
    selected_category_name = st.selectbox(
        "Select Tweet Category:",
        options=category_names,
        key="new_tweet_category_select"
    )
    logger.debug(f"Selected category name from dropdown: {selected_category_name}")

    selected_category: Optional[TweetCategory] = None
    for cat in AVAILABLE_CATEGORIES:
        if cat.name == selected_category_name:
            selected_category = cat
            break
    
    if selected_category:
        st.caption(selected_category.description)
        # Display keywords and style guidelines for the selected category
        with st.expander("Category Details & Guidelines", expanded=False):
            st.markdown(f"**Keywords:** {', '.join(selected_category.prompt_keywords) if selected_category.prompt_keywords else 'N/A'}")
            st.markdown("**Style Guidelines:**")
            if selected_category.style_guidelines:
                for key, value in selected_category.style_guidelines.items():
                    st.markdown(f"  - **{key.replace('_', ' ').capitalize()}:** {value}")
            else:
                st.markdown("  - N/A")

    topic_brief = st.text_area(
        "Topic or Key Points for the Tweet:",
        placeholder="Enter a brief topic, key message, or specific points to include...",
        key="new_tweet_topic_input",
        height=100
    )

    # Option to generate a poster image
    generate_image = st.checkbox("Generate Poster Image", key="generate_image_new_tweet")
    if st.button("Generate New Tweet", key="generate_new_tweet_button"):
        logger.info("'Generate New Tweet' button clicked.")
        if not selected_category:
            logger.warning("No category selected by user.")
            st.error("Please select a valid category.")
            return
        
        logger.info(f"Selected category for generation: {selected_category.name}")
        logger.info(f"Topic/Key Points provided by user: '{topic_brief.strip()}'")

        if not topic_brief.strip():
            logger.warning("No topic/key points provided. Generating a generic tweet for the category.")
            # Proceed with None topic if user doesn't provide one, 
            # or enforce it by returning here if a topic is mandatory.
            # topic_brief = None # If you want to explicitly pass None

        with st.spinner(f"Generating new '{selected_category.name}' tweet..."):
            try:
                logger.info(f"Calling generate_new_tweet with category='{selected_category.name}', persona='{active_account_type.value}', topic='{topic_brief.strip() if topic_brief.strip() else None}'")
                
                # Show progress steps
                progress = st.progress(0)
                st.text("Step 1/3: Creating persona and preparing context...")
                progress.progress(25)
                time.sleep(0.5)
                # Create an Account object for the active persona
                active_account = Account(
                    account_id=f"yieldfi_{active_account_type.value.lower()}",
                    username=f"YieldFi{active_account_type.value.capitalize()}",
                    display_name=f"YieldFi {active_account_type.value.capitalize()}",
                    account_type=active_account_type,
                    platform="Twitter",
                    follower_count=100000, # Placeholder
                    bio="YieldFi Agent Account", # Placeholder
                    interaction_history=[],
                    tags=[]
                )
                
                st.text("Step 2/3: Retrieving knowledge for the topic...")
                progress.progress(50)
                time.sleep(0.5)
                
                st.text("Step 3/3: Generating AI content...")
                progress.progress(90)
                
                response = generate_new_tweet(
                    category=selected_category,
                    responding_as=active_account,
                    topic=topic_brief.strip() if topic_brief.strip() else None, # Pass None if empty
                    generate_image=generate_image
                )
                progress.progress(100)
                logger.info(f"Received response from generate_new_tweet. Model used: {response.model_used}")
                logger.debug(f"Raw response content from generate_new_tweet: '{response.content}'")
                
                # Store in session state for display
                st.session_state.generated_new_tweet_content = response.content
                st.session_state.generated_new_tweet_model = response.model_used
                st.session_state.full_new_tweet_response = response
                
                # Get character count for verification
                char_count = len(response.content)
                if char_count > 280:
                    st.warning(f"⚠️ Tweet exceeds Twitter's 280 character limit! Current length: {char_count} characters")
                else:
                    st.info(f"✓ Tweet length: {char_count}/280 characters")
                # Potentially add other response attributes like tone_analysis if relevant for new tweets
                # and if AIResponse model is updated to include it for new tweets.

            except APIError as ae: # Catch APIError specifically
                logger.error(f"APIError generating new tweet in UI: {str(ae)}", exc_info=True)
                st.session_state.generated_new_tweet_content = None
                st.session_state.generated_new_tweet_error = f"API Error: {str(ae)}" # More specific error message
                st.error(st.session_state.generated_new_tweet_error)
            except Exception as e:
                logger.error(f"Error generating new tweet in UI: {str(e)}", exc_info=True)
                st.session_state.generated_new_tweet_content = None
                st.session_state.generated_new_tweet_error = f"An unexpected error occurred: {str(e)}"
                st.error(st.session_state.generated_new_tweet_error)

    # Display generated tweet or error
    if "generated_new_tweet_content" in st.session_state and st.session_state.generated_new_tweet_content:
        st.markdown("**AI-Generated New Tweet:**")
        # The warning you are seeing might be coming from here if the content is not as expected.
        # Let's log what's being displayed.
        tweet_to_display = st.session_state.generated_new_tweet_content
        logger.info(f"Displaying generated tweet: '{tweet_to_display}'")
        if "[Warning:" in tweet_to_display or not tweet_to_display.strip(): # Basic check for problematic content
            logger.warning(f"Potential issue with generated tweet content: '{tweet_to_display}'")
            st.warning(f"AI response might have an issue: {tweet_to_display}") # Display a warning if it looks problematic
        else:
            st.success(tweet_to_display)
        
        copy_button(tweet_to_display, button_text="Copy Tweet Text")
        if st.session_state.get("generated_new_tweet_model"):
            st.caption(f"Generated using: {st.session_state.generated_new_tweet_model}")
        
        # Add debug information in an expandable section
        if "full_new_tweet_response" in st.session_state:
            with st.expander("Debug Information", expanded=False):
                st.markdown("**Response Generation Details:**")
                st.text(f"Model Used: {st.session_state.full_new_tweet_response.model_used}")
                st.text(f"Generated at: {st.session_state.full_new_tweet_response.generation_time}")
                st.text(f"Character Count: {len(st.session_state.full_new_tweet_response.content)}")
                st.text(f"Response Type: {st.session_state.full_new_tweet_response.response_type}")
                st.text(f"Category: {selected_category_name}")
                if hasattr(st.session_state.full_new_tweet_response, 'extra_context') and st.session_state.full_new_tweet_response.extra_context:
                    st.text("Extra Context:")
                    st.json(st.session_state.full_new_tweet_response.extra_context)
                # Show prompt if in debug mode
                if st.session_state.full_new_tweet_response.prompt_used:
                    with st.expander("Show Prompt Used", expanded=False):
                        st.code(st.session_state.full_new_tweet_response.prompt_used, language="markdown")
        
        # Display generated poster image if available
        if hasattr(st.session_state.full_new_tweet_response, 'image_url') and st.session_state.full_new_tweet_response.image_url:
            st.markdown("**Generated Poster Image:**")
            st.image(st.session_state.full_new_tweet_response.image_url, caption="Poster Image")
            copy_button(st.session_state.full_new_tweet_response.image_url, button_text="Copy Image URL")
    
    elif "generated_new_tweet_error" in st.session_state and st.session_state.generated_new_tweet_error and not st.session_state.get("generated_new_tweet_content"):
        # This handles the case where an error occurred and spinner was exited, but no content was generated.
        # The error might have already been displayed within the button logic, but this is a fallback.
        if not st.session_state.get("_new_tweet_error_displayed_main_"):
             st.error(f"Failed to generate tweet: {st.session_state.generated_new_tweet_error}")
             st.session_state._new_tweet_error_displayed_main_ = True # Avoid double display
    else:
        # Clear flag if no error or content currently being displayed
        if "_new_tweet_error_displayed_main_" in st.session_state:
            del st.session_state._new_tweet_error_displayed_main_

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

    display_category_tweet_ui(selected_account_type)

    st.markdown("---")
    st.write("Note: This is a direct run of category_select.py. Full app functionality might differ.")
    st.write("Ensure `data/input/categories.json` exists and is populated for full category options.")

    # Clean up dummy file if created
    # This cleanup logic is tricky with Streamlit's execution model on direct run.
    # Manual cleanup might be needed if you stop the script early.
    # Consider not auto-creating for direct run to avoid complexity. 