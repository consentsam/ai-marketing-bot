# Changelog:
# 2025-05-07 21:10 - Step 15.1 - Implemented tweet input interface UI.
# 2025-05-07 21:20 - Step 15.2 - Added target account metadata inputs and integration into reply generation.

from typing import Optional
import streamlit as st
import time
from datetime import datetime, timezone

from src.data_sources.mock import MockTweetDataSource
from src.ai.response_generator import generate_tweet_reply
from src.models.tweet import Tweet
from src.models.account import Account, AccountType
from src.ui.components import status_badge, collapsible_container, copy_button
from src.utils.logging import get_logger

# Initialize logger
logger = get_logger(__name__)

# Initialize the mock data source once
mock_data_source = MockTweetDataSource()

def display_tweet_reply_ui(active_account_type: AccountType):
    """User interface for generating tweet replies."""
    st.subheader("Generate Tweet Reply")

    # Input fields
    tweet_url = st.text_input("Tweet URL (e.g., https://twitter.com/user/status/1234567890)", key="reply_tweet_url")
    manual_content = st.text_area("Or paste tweet content manually", key="reply_tweet_content")

    # Input for manual author metadata when manual content is used
    manual_author_username = None
    manual_author_type = None
    if manual_content:
        manual_author_username = st.text_input("Original Author Username (e.g., @user)", key="reply_author_username")
        manual_author_type_str = st.selectbox(
            "Original Author Account Type:",
            options=[atype.value for atype in AccountType],
            key="reply_author_type"
        )
        manual_author_type = AccountType(manual_author_type_str)

    # Determine which content to use
    tweet_obj: Optional[Tweet] = None
    target_account: Optional[Account] = None
    if tweet_url:
        try:
            tweet_obj = mock_data_source.get_tweet_by_url(tweet_url)
            if not tweet_obj:
                st.error("No tweet found for the provided URL.")
            else:
                st.markdown("**Fetched Tweet Content:**")
                st.write(tweet_obj.content)
                # Fetch target account info from mock data source
                if tweet_obj.metadata.author_username:
                    target_account = mock_data_source.get_account_by_username(tweet_obj.metadata.author_username)
                    if target_account:
                        st.markdown(f"**Original Author:** @{target_account.username} ({target_account.account_type.value})")
                    else:
                        st.warning("Original author account not found in mock data source.")
        except Exception as e:
            st.error(f"Error retrieving tweet by URL: {e}")
    elif manual_content:
        # Build a manual Tweet object
        tweet_obj = Tweet(content=manual_content.strip())
        st.markdown("**Manual Tweet Content:**")
        st.write(tweet_obj.content)
        # Build manual target account if provided
        if manual_author_username and manual_author_type:
            target_account = Account(
                account_id="manual_" + manual_author_username,
                username=manual_author_username,
                display_name=manual_author_username,
                account_type=manual_author_type,
                platform="Twitter",
                follower_count=0,
                bio="",
                interaction_history=[],
                tags=[]
            )
            st.markdown(f"**Original Author:** @{target_account.username} ({target_account.account_type.value})")
        else:
            st.info("Provide the original author username and type above to include metadata in response generation.")

    # Option to generate a poster image
    generate_image = st.checkbox("Generate Poster Image", key="generate_image_reply")
    # Button to generate reply
    if tweet_obj:
        if st.button("Generate Reply", key="generate_reply_button"):
            if not tweet_obj:
                st.error("No valid tweet data to process. Please check inputs.")
                return

            with st.spinner("Generating AI reply..."):
                try:
                    # Get the selected persona/account type for responding
                    # Create an Account object for the active persona
                    st.info("Creating YieldFi persona based on selected account type...")
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
                    if not active_account:
                        st.error(f"Could not determine a valid AccountType for responding. Please check configuration.")
                        st.session_state.generated_reply = ""
                        return

                    # Show progress steps
                    progress = st.progress(0)
                    st.text("Step 1/4: Generating prompt...")
                    progress.progress(25)
                    time.sleep(0.5)
                    st.text("Step 2/4: Analyzing tone...")
                    progress.progress(50)
                    time.sleep(0.5)
                    st.text("Step 3/4: Retrieving knowledge...")
                    progress.progress(75)
                    time.sleep(0.5)
                    st.text("Step 4/4: Generating AI response...")
                    progress.progress(100)

                    response = generate_tweet_reply(
                        original_tweet=tweet_obj,
                        responding_as=active_account,
                        target_account=target_account,
                        generate_image=generate_image
                    )
                    # Check if response has an error attribute, which was removed earlier
                    # For now, assume content will indicate error if one occurred based on response_generator logic
                    # if hasattr(response, 'error') and response.error:
                    #    st.error(f"Error generating reply: {response.error}")
                    #    st.session_state.generated_reply = ""
                    if "[Error:" in response.content or "[Warning:" in response.content:
                        st.error(f"Error generating reply: {response.content}")
                        st.session_state.generated_reply = ""
                    else:
                        st.session_state.generated_reply = response.content
                        st.session_state.generated_tone = response.tone # Direct attribute now
                        st.session_state.full_ai_response = response
                        
                        # Get character count for verification
                        char_count = len(response.content)
                        if char_count > 280:
                            st.warning(f"⚠️ Tweet exceeds Twitter's 280 character limit! Current length: {char_count} characters")
                        else:
                            st.info(f"✓ Tweet length: {char_count}/280 characters")
                
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
                    logger.error(f"Unexpected error in UI while generating reply: {str(e)}", exc_info=True)
                    st.session_state.generated_reply = ""

    if "generated_reply" in st.session_state and st.session_state.generated_reply:
        # Display tone above the tweet box
        st.markdown(f"**Tone:** {st.session_state.generated_tone or 'N/A'}")
        # Display only the tweet content in a text area
        st.text_area(label="", value=st.session_state.generated_reply, key="generated_tweet_display", height=100)
        copy_button(st.session_state.generated_reply) # Added copy button back for the text

        # Display generated poster image if available
        if hasattr(st.session_state, 'full_ai_response') and st.session_state.full_ai_response and hasattr(st.session_state.full_ai_response, 'image_url') and st.session_state.full_ai_response.image_url:
            logger.info(f"Displaying poster image. URL: {st.session_state.full_ai_response.image_url}")
            st.markdown("**Generated Poster Image:**")
            st.image(st.session_state.full_ai_response.image_url, caption="Poster Image")
            copy_button(st.session_state.full_ai_response.image_url) # Copy button for image URL
        elif generate_image: # Check if image was requested but not generated
             logger.warning("Image was requested, but no image_url found in session state.")
             st.warning("Poster image was requested but could not be generated or found.")

        # Add debug information in an expandable section
        with st.expander("Debug Information", expanded=False):
            st.markdown("**Response Generation Details:**")
            if hasattr(st.session_state, 'full_ai_response') and st.session_state.full_ai_response:
                response_obj = st.session_state.full_ai_response
                st.text(f"Model Used: {response_obj.model_used}")
                st.text(f"Generated at: {response_obj.generation_time}")
                st.text(f"Character Count: {len(response_obj.content)}")
                st.text(f"Response Type: {response_obj.response_type}")
                st.text(f"Image URL in AIResponse: {response_obj.image_url if hasattr(response_obj, 'image_url') else 'N/A'}")
                if hasattr(response_obj, 'extra_context') and response_obj.extra_context:
                    st.text("Extra Context Provided to AI:")
                    st.json(response_obj.extra_context)
                st.text("Full AI Prompt Used:")
                st.text_area("Prompt", value=response_obj.prompt_used, height=150, key="debug_prompt_used_reply")
            else:
                st.text("No full AI response object found in session state for debugging.") 