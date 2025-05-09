# Changelog:
# 2025-05-07 21:10 - Step 15.1 - Implemented tweet input interface UI.
# 2025-05-07 21:20 - Step 15.2 - Added target account metadata inputs and integration into reply generation.
# 2025-05-19 12:45 - Step 25 - Added support for interaction modes.

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

def display_tweet_reply_ui(active_account_type: AccountType, interaction_mode: str = "Default"):
    """
    User interface for generating tweet replies.
    
    Args:
        active_account_type: The account type to respond as (Official, Intern, etc.)
        interaction_mode: The interaction mode to use (Default, Professional, Degen)
    """
    st.subheader("Generate Tweet Reply")
    logger.info(f"Displaying tweet reply UI with interaction mode: {interaction_mode}")

    # Display the selected interaction mode
    st.info(f"Using interaction mode: {interaction_mode}")

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
                    try:
                        # Show progress
                        with st.spinner("Generating AI response..."):
                            # Log detailed information about the request
                            logger.info(f"Generating tweet reply request details:")
                            logger.info(f"  - Active account type: {active_account_type.value}")
                            logger.info(f"  - Interaction mode: {interaction_mode}")
                            logger.info(f"  - Original tweet content: '{tweet_obj.content[:100]}...'")
                            logger.info(f"  - Target account: {target_account.username if target_account else 'None'}")
                            logger.info(f"  - Generate image: {generate_image}")
                            
                            # Call the generator function
                            response = generate_tweet_reply(
                                original_tweet=tweet_obj,
                                responding_as=active_account,
                                target_account=target_account,
                                generate_image=generate_image,
                                interaction_mode=interaction_mode
                            )
                            
                            # Validate response isn't just echoing input
                            if response.content.strip().lower() == tweet_obj.content.strip().lower():
                                logger.error(f"CRITICAL BUG: Response is identical to input tweet despite validation!")  
                                st.error("Error: The generated response was identical to the input. Please try again or modify your input.")
                                st.session_state.generated_reply = "[Error: Generated response matched input tweet exactly]"  
                            elif "[Error: AI returned input tweet without changes]" in response.content:
                                logger.error(f"AI model returned input tweet - caught by response_generator validation")
                                st.error("Error: The AI model returned the input tweet. This is an issue with the API response. Please try again or modify your input.")
                                st.session_state.generated_reply = response.content
                            else:
                                logger.info(f"Successfully generated unique response, length: {len(response.content)} chars")
                    except Exception as e:
                        st.error(f"An unexpected error occurred: {str(e)}")
                        logger.error(f"Unexpected error in UI while generating reply: {str(e)}", exc_info=True)
                    if "[Error:" in response.content or "[Warning:" in response.content:
                        st.error(f"Error generating reply: {response.content}")
                        st.session_state.generated_reply = ""
                    else:
                        st.session_state.generated_reply = response.content
                        st.session_state.generated_tone = response.tone # Direct attribute now
                        st.session_state.full_ai_response = response
                        
                        # Get character count for verification
                        char_count = len(response.content)
                        
                        # Log response details
                        logger.info(f"Generated response details:")
                        logger.info(f"  - Character count: {char_count}/280")
                        logger.info(f"  - Response starts with: '{response.content[:50]}...'")
                        logger.info(f"  - Model used: {response.model_used}")
                        logger.info(f"  - Image generated: {response.image_url is not None}")
                        
                        if char_count > 280:
                            logger.warning(f"Generated tweet exceeds character limit: {char_count} > 280")
                            st.warning(f"⚠️ Tweet exceeds Twitter's 280 character limit! Current length: {char_count} characters")
                        else:
                            logger.info(f"Generated tweet within character limit: {char_count} <= 280")
                            st.info(f"✓ Tweet length: {char_count}/280 characters")
                
                except Exception as e:
                    st.error(f"An unexpected error occurred: {str(e)}")
                    logger.error(f"Unexpected error in UI while generating reply: {str(e)}", exc_info=True)
                    st.session_state.generated_reply = ""

    if "generated_reply" in st.session_state and st.session_state.generated_reply:
        # Display tone above the tweet box
        st.markdown(f"**Tone:** {st.session_state.generated_tone or 'N/A'}")
        
        # Basic validation of tweet content
        generated_content = st.session_state.generated_reply
        
        # Perform input-output comparison for extra validation
        if tweet_obj and tweet_obj.content and generated_content.strip().lower() == tweet_obj.content.strip().lower():
            logger.error(f"FINAL VALIDATION CATCH: Output is identical to input despite all checks!")
            st.error("Critical Error: Generated content is identical to input tweet. This should not happen - the system will not display identical content as it could be confusing.")
        elif generated_content.strip() == "" or "[Error:" in generated_content or "[Warning:" in generated_content:
            logger.warning(f"Error/warning in generated reply: {generated_content}")
            st.error(f"Error in generated reply: {generated_content}")
        else:
            # Success path - valid, unique response
            logger.info(f"Displaying successful tweet reply: '{generated_content[:50]}...'")
            
            # Use st.success for better visual highlighting of the tweet
            st.success(generated_content)
            
            # Add character count validation
            char_count = len(generated_content)
            st.info(f"✓ Tweet length: {char_count}/280 characters")
            
            # Add copy button for easy copying
            copy_button(generated_content, "Copy Tweet")

        # Display generated poster image if available
        if hasattr(st.session_state, 'full_ai_response') and st.session_state.full_ai_response and hasattr(st.session_state.full_ai_response, 'image_url') and st.session_state.full_ai_response.image_url:
            logger.info(f"Displaying poster image. URL: {st.session_state.full_ai_response.image_url}")
            st.markdown("**Generated Poster Image:**")
            st.image(st.session_state.full_ai_response.image_url, caption="Poster Image")
            copy_button(st.session_state.full_ai_response.image_url, "Copy Image URL") # Updated button text
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
                st.text(f"Interaction Mode: {interaction_mode}")  # Display the interaction mode
                st.text(f"Image URL in AIResponse: {response_obj.image_url if hasattr(response_obj, 'image_url') else 'N/A'}")
                if hasattr(response_obj, 'extra_context') and response_obj.extra_context:
                    st.text("Extra Context Provided to AI:")
                    st.json(response_obj.extra_context)
                st.text("Full AI Prompt Used:")
                st.text_area("Prompt", value=response_obj.prompt_used, height=150, key="debug_prompt_used_reply")
            else:
                st.text("No full AI response object found in session state for debugging.") 