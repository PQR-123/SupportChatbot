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

def display_chat_history():
    """Display the chat history with custom styling."""
    for message in st.session_state.messages:
        if message["role"] == "user":
            st.write(f'🧑‍💻 **You:** {message["content"]}')
        elif message["role"] == "assistant":
            st.write(f'🤖 **Assistant:** {message["content"]}')
        elif message["role"] == "error":
            st.error(message["content"])

def format_response(results: List[str], cdp: str = None) -> str:
    """Format search results into a coherent response."""
    if not results:
        return ("I couldn't find a specific answer to your question. "
                "Please try rephrasing or ask about a different aspect of CDP.")
    
    response = "Here's what I found:\n\n"
    for idx, result in enumerate(results, 1):
        response += f"{idx}. {result}\n\n"
    
    if cdp:
        response += f"\nThis information is specific to {cdp.capitalize()}. "
    else:
        response += "\nThis is general CDP information. "
    
    return response
