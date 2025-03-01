import streamlit as st
from src.document_store import DocumentStore
from src.text_processor import TextProcessor
from src.chat_utils import (
    init_session_state, 
    add_message, 
    display_chat_history, 
    format_response
)
from src.cdp_data import SAMPLE_DATA

# Page configuration
st.set_page_config(
    page_title="CDP Support Chatbot",
    page_icon="🤖",
    layout="wide"
)

# Custom CSS
st.markdown("""
    <style>
    .stTextInput > div > div > input {
        background-color: #f0f2f6;
        color: black !important;
    }
    .stButton > button {
        width: 100%;
    }
    div[data-testid="stMarkdownContainer"] strong:has(+ em:contains("You")) + em {
        color: black !important;
        font-style: normal;
    }
    </style>
    """, unsafe_allow_html=True)

def initialize_document_store():
    """Initialize and populate document store."""
    if st.session_state.document_store is None:
        doc_store = DocumentStore()
        for cdp, content in SAMPLE_DATA.items():
            doc_store.add_document(cdp, content)
        st.session_state.document_store = doc_store

def main():
    # Initialize session state and document store
    init_session_state()
    initialize_document_store()

    # Header
    st.title("CDP Support Assistant 🤖")
    st.markdown("""
    Ask me how-to questions about:
    - Segment
    - mParticle
    - Lytics
    - Zeotap
    """)

    # Initialize text processor
    text_processor = TextProcessor()

    # Chat interface
    with st.container():
        # Display existing chat history
        display_chat_history()

        # Question input
        question = st.text_input(
            "Ask your question:",
            key="question_input",
            placeholder="How do I set up a new source in Segment?"
        )

        # Process new question
        if question and question not in [msg["content"] for msg in st.session_state.messages if msg["role"] == "user"]:
            # Validate question
            is_valid, error_msg = text_processor.validate_question(question)

            if not is_valid:
                add_message("error", error_msg)
            else:
                # Add user question to chat
                add_message("user", question)

                with st.spinner("Searching for answer..."):
                    # Extract CDP if mentioned
                    cdp = text_processor.extract_cdp(question)

                    # Search for relevant information
                    results = st.session_state.document_store.search(
                        question, cdp
                    )

                    # Format and display response
                    response = format_response(results, cdp if cdp else "general")
                    add_message("assistant", response)

    # Footer
    st.markdown("---")
    st.markdown(
        "This chatbot helps with CDP-related how-to questions. "
        "For complex issues, please refer to the official documentation."
    )

if __name__ == "__main__":
    main()