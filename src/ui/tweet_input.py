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

    # Button to generate reply
    if tweet_obj:
        if st.button("Generate Reply", key="generate_reply_button"):
            if not tweet_obj:
                st.error("No valid tweet data to process. Please check inputs.")
                return

            with st.spinner("Generating AI reply..."):
                try:
                    # Get the selected persona/account type for responding
                    active_account_type_enum = active_account_type
                    if not active_account_type_enum:
                        st.error(f"Could not determine a valid AccountType for responding. Please check configuration.")
                        st.session_state.generated_reply = ""
                        return

                    response = generate_tweet_reply(
                        original_tweet=tweet_obj,
                        responding_as_type=active_account_type_enum,
                        target_account=target_account,
                    )
                    if response.error:
                        st.error(f"Error generating reply: {response.error}")
                        st.session_state.generated_reply = ""
                    else:
                        st.session_state.generated_reply = response.reply
                        st.session_state.generated_tone = response.tone_analysis.get("main_tone", "N/A") if response.tone_analysis else "N/A"
                        st.session_state.full_ai_response = response
                
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
                    logger.error(f"Unexpected error in UI while generating reply: {str(e)}", exc_info=True)
                    st.session_state.generated_reply = ""

    if "generated_reply" in st.session_state and st.session_state.generated_reply:
        st.markdown("**AI-Generated Reply:**")
        st.success(st.session_state.generated_reply)
        status_badge("Tone", st.session_state.generated_tone or "N/A")
        copy_button(st.session_state.generated_reply) 