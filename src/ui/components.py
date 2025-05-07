# Changelog:
# 2025-05-07 21:05 - Step 14.1 - Created UI components file with placeholder and basic utility components.

"""
UI Components for YieldFi AI Agent.

Purpose: Provides reusable UI components for the YieldFi AI Agent Streamlit application.
Rationale: Centralizing UI components improves code reuse and maintainability.
Usage: Import components in app.py and use them in your UI functions.
TODOs:
    - Add tweet display component for Step 15
    - Add response display component for Step 16
    - Add category selection component for Step 19
"""

import streamlit as st
from typing import Optional, Dict, Any

def placeholder_component(title: str, message: str, icon: str = "ℹ️"):
    """
    Display a placeholder component for features not yet implemented.
    
    Args:
        title: Title of the placeholder
        message: Message to display
        icon: Emoji icon to use
    """
    with st.container():
        st.markdown(f"### {icon} {title}")
        st.info(message)

def status_badge(label: str, status: str):
    """
    Display a colorful status badge.
    
    Args:
        label: The label text
        status: One of "success", "warning", "error", "info"
    """
    colors = {
        "success": "#28a745",
        "warning": "#ffc107",
        "error": "#dc3545",
        "info": "#17a2b8"
    }
    color = colors.get(status.lower(), colors["info"])
    st.markdown(
        f"""
        <div style="
            display: inline-block;
            padding: 0.25em 0.4em;
            font-size: 0.9em;
            font-weight: 700;
            line-height: 1;
            text-align: center;
            white-space: nowrap;
            vertical-align: baseline;
            border-radius: 0.25rem;
            background-color: {color};
            color: white;
        ">
            {label}
        </div>
        """, 
        unsafe_allow_html=True
    )

def collapsible_container(header: str, content_func, default_expanded: bool = False):
    """
    Create a collapsible container with custom content.
    
    Args:
        header: Header text for the container
        content_func: Function that generates the content (called only if expanded)
        default_expanded: Whether the container is expanded by default
    """
    expanded = st.expander(header, expanded=default_expanded)
    with expanded:
        content_func()

def copy_button(text: str, button_text: str = "Copy"):
    """
    Create a button that copies text to clipboard when clicked.
    
    Args:
        text: Text to copy
        button_text: Text to display on the button
    """
    st.markdown(
        f"""
        <div class="stButton">
            <button onclick="navigator.clipboard.writeText('{text}'); this.innerHTML='Copied!'; setTimeout(() => this.innerHTML='{button_text}', 1500);" class="css-1ubiltw edgvbvh9">
                {button_text}
            </button>
        </div>
        """,
        unsafe_allow_html=True
    )

# Example usage in __main__ for testing
if __name__ == "__main__":
    st.set_page_config(page_title="UI Components Test", layout="wide")
    st.title("UI Components Test")
    
    placeholder_component("Test Component", "This component is a placeholder for future functionality")
    
    st.write("Status badges:")
    status_badge("Success", "success")
    status_badge("Warning", "warning")
    status_badge("Error", "error")
    status_badge("Info", "info")
    
    def content_generator():
        st.write("This content is inside the collapsible container.")
        st.code("print('Hello from collapsible container')")
    
    collapsible_container("Click to expand", content_generator)
    
    st.write("Copy button test:")
    copy_button("This text will be copied to clipboard") 