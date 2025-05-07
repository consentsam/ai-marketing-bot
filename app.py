# src/app.py (or app.py at root, depending on final structure for Streamlit execution)
# Changelog:
# 2025-05-06 HH:MM - Step 14 (Initial) - Basic structure for YieldFi AI Agent Streamlit app.
# 2025-05-07 21:00 - Step 14 (Complete) - Uncommented imports and UI structure for the main application.
# 2025-05-07 HH:MM - Step 19 - Integrated category selection UI.

"""
YieldFi AI Agent Streamlit Application.

Purpose: Provides a user interface for interacting with the YieldFi AI Agent,
         allowing users to generate tweet replies, create new tweets by category,
         and potentially other future interactions as per the roadmap.
Rationale: A user-friendly interface is needed to make the AI agent's
           capabilities accessible.
Usage: Run with `streamlit run app.py` (or `streamlit run src/app.py`).
TODOs:
    - Connect UI elements to backend modules (response_generator, data_sources)
"""

import streamlit as st
from dotenv import load_dotenv

from src.config.settings import load_config, get_config # get_config might not be directly used here but good to have
from src.ai.response_generator import generate_tweet_reply, generate_new_tweet
from src.data_sources.mock import MockTweetDataSource
from src.models.tweet import Tweet
from src.models.account import Account, AccountType
from src.ui.components import status_badge, placeholder_component, copy_button
from src.ui.tweet_input import display_tweet_reply_ui
from src.ui.category_select import display_new_tweet_by_category_ui # ADDED FOR STEP 19

def main():
    """
    Main function to run the Streamlit application.
    """
    load_dotenv()
    load_config()  # Load application configuration

    st.set_page_config(
        page_title="YieldFi AI Agent",
        page_icon="🤖", # Or a YieldFi specific icon
        layout="wide"
    )

    st.title("YieldFi AI Agent 🤖")
    st.markdown("""
    Generate Twitter replies and new tweets with AI assistance.
    This agent understands YieldFi's core messaging and adapts to different persona types.
    """)

    # --- Sidebar for Configuration/Mode Selection ---
    st.sidebar.header("Agent Configuration")
    active_account_type_str = st.sidebar.selectbox(
        "Respond as:",
        options=[
            AccountType.OFFICIAL.value, 
            AccountType.INTERN.value,
            # Add other relevant personas for selection later e.g. PARTNER, KOL
        ],
        key="active_account_persona_select"
    )
    active_account_type = AccountType(active_account_type_str)
    
    # Display basic account info
    st.sidebar.markdown(f"**Selected Persona:** {active_account_type_str}")
    if active_account_type == AccountType.OFFICIAL:
        st.sidebar.markdown("*The official YieldFi voice - professional, authoritative, and informative.*")
    elif active_account_type == AccountType.INTERN:
        st.sidebar.markdown("*A friendly, enthusiastic voice - approachable and conversational.*")
    # Add descriptions for other personas if they are added to the selectbox

    # --- Main Interaction Area ---
    interaction_type = st.radio(
        "Select Interaction Type:",
        ("Generate Tweet Reply", "Create New Tweet by Category"),
        key="interaction_type_radio"
    )

    if interaction_type == "Generate Tweet Reply":
        display_tweet_reply_ui(active_account_type)
    elif interaction_type == "Create New Tweet by Category":
        display_new_tweet_by_category_ui(active_account_type) # UPDATED FOR STEP 19

    # Footer
    st.markdown("---")
    st.caption("YieldFi AI Agent - Powered by Langchain and xAI (Conceptual)") # Updated placeholder

if __name__ == "__main__":
    main()