from typing import List, Dict, Any
import streamlit as st

def init_session_state():
    """Initialize session state variables."""
    if 'messages' not in st.session_state:
        st.session_state.messages = []
    if 'document_store' not in st.session_state:
        st.session_state.document_store = None

def add_message(role: str, content: str):
    """Add a message to the chat history."""
    st.session_state.messages.append({"role": role, "content": content})
    # Force a rerun to update the display
    st.rerun()

def display_chat_history():
    """Display the chat history with custom styling."""
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.markdown(f'**_You:_** {message["content"]}')
        elif message["role"] == "assistant":
            st.markdown(f'**Assistant:** {message["content"]}')
        elif message["role"] == "error":
            st.error(message["content"])

def format_response(results: List[str], cdp: str = None) -> str:
    """Format search results into a coherent response."""
    if not results:
        return ("I couldn't find a specific answer to your question. "
                "Please try rephrasing or ask about a different aspect of CDP.")

    # Join results with proper formatting
    response_parts = []
    for idx, result in enumerate(results, 1):
        response_parts.append(f"{idx}. {result.strip()}")

    response = "Here's what I found:\n\n" + "\n\n".join(response_parts)

    if cdp:
        response += f"\n\nThis information is specific to {cdp.capitalize()}."
    else:
        response += "\n\nThis is general CDP information."

    return response