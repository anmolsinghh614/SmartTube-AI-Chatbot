import os
import tempfile
import streamlit as st
from streamlit_chat import message
from youtubequery import YoutubeQuery
import re

st.set_page_config(page_title="Youtube to Chatbot", page_icon="🎥")


def is_valid_youtube_url(url):
    """Validate if the URL is a valid YouTube URL"""
    youtube_regex = r'(?:https?://)?(?:www\.)?(?:youtube\.com/watch\?v=|youtu\.be/)([a-zA-Z0-9_-]{11})'
    return bool(re.match(youtube_regex, url))


def is_valid_openai_api_key(api_key):
    """Basic validation for OpenAI API key format"""
    return api_key.startswith('sk-') and len(api_key) > 20


def display_messages():
    st.subheader("Chat")
    for i, (msg, is_user) in enumerate(st.session_state["messages"]):
        message(msg, is_user=is_user, key=str(i))
    st.session_state["thinking_spinner"] = st.empty()


def process_input():
    if st.session_state["user_input"] and len(st.session_state["user_input"].strip()) > 0:
        user_text = st.session_state["user_input"].strip()
        
        if not st.session_state.get("db_loaded", False):
            st.error("Please add a YouTube video first before asking questions.")
            return
            
        with st.session_state["thinking_spinner"], st.spinner(f"Thinking..."):
            try:
                query_text = st.session_state["youtubequery"].ask(user_text)
                st.session_state["messages"].append((user_text, True))
                st.session_state["messages"].append((query_text, False))
            except Exception as e:
                st.error(f"Error processing your question: {str(e)}")
                st.session_state["messages"].append((user_text, True))
                st.session_state["messages"].append(("Sorry, I encountered an error while processing your question. Please try again.", False))


def ingest_input():
    if st.session_state["input_url"] and len(st.session_state["input_url"].strip()) > 0:
        url = st.session_state["input_url"].strip()
        
        if not is_valid_youtube_url(url):
            st.error("Please enter a valid YouTube URL.")
            return
            
        with st.session_state["thinking_spinner"], st.spinner(f"Processing video..."):
            try:
                ingest_text = st.session_state["youtubequery"].ingest(url)
                if ingest_text == "Success":
                    st.success("Video processed successfully! You can now ask questions about it.")
                    st.session_state["db_loaded"] = True
                    st.session_state["current_video"] = url
                else:
                    st.error("Failed to process video. Please check the URL and try again.")
            except Exception as e:
                st.error(f"Error processing video: {str(e)}")
                st.info("Make sure the video has captions/transcripts available.")


def is_openai_api_key_set() -> bool:
    return len(st.session_state["OPENAI_API_KEY"]) > 0 and is_valid_openai_api_key(st.session_state["OPENAI_API_KEY"])


def main():
    if len(st.session_state) == 0:
        st.session_state["messages"] = []
        st.session_state["url"] = ""
        st.session_state["db_loaded"] = False
        st.session_state["current_video"] = ""
        st.session_state["OPENAI_API_KEY"] = os.environ.get("OPENAI_API_KEY", "")
        if is_openai_api_key_set():
            st.session_state["youtubequery"] = YoutubeQuery(st.session_state["OPENAI_API_KEY"])
        else:
            st.session_state["youtubequery"] = None

    st.header("🎥 YouTube to Chatbot")
    st.markdown("Chat with any YouTube video using AI!")

    # API Key Input
    api_key_input = st.text_input(
        "OpenAI API Key", 
        value=st.session_state["OPENAI_API_KEY"], 
        key="input_OPENAI_API_KEY", 
        type="password",
        help="Enter your OpenAI API key. It should start with 'sk-'"
    )
    
    if api_key_input:
        if (
            len(api_key_input) > 0
            and api_key_input != st.session_state["OPENAI_API_KEY"]
        ):
            if is_valid_openai_api_key(api_key_input):
                st.session_state["OPENAI_API_KEY"] = api_key_input
                st.session_state["messages"] = []
                st.session_state["user_input"] = ""
                st.session_state["input_url"] = ""
                st.session_state["db_loaded"] = False
                st.session_state["youtubequery"] = YoutubeQuery(st.session_state["OPENAI_API_KEY"])
                st.success("API key updated successfully!")
            else:
                st.error("Invalid OpenAI API key format. Please check your key.")

    # URL Input Section
    st.subheader("📹 Add a YouTube Video")
    
    if st.session_state.get("current_video"):
        st.info(f"Currently loaded: {st.session_state['current_video']}")
        if st.button("Load Different Video"):
            st.session_state["db_loaded"] = False
            st.session_state["current_video"] = ""
            st.session_state["messages"] = []
            st.rerun()
    
    url_input = st.text_input(
        "YouTube URL", 
        value=st.session_state["url"], 
        key="input_url", 
        disabled=not is_openai_api_key_set(),
        placeholder="https://www.youtube.com/watch?v=...",
        on_change=ingest_input,
        help="Paste a YouTube video URL to start chatting about it"
    )

    st.session_state["ingestion_spinner"] = st.empty()

    # Chat Section
    if st.session_state.get("db_loaded", False):
        st.subheader("💬 Chat with the Video")
        display_messages()
        
        user_input = st.text_input(
            "Ask a question about the video", 
            key="user_input", 
            disabled=not is_openai_api_key_set(),
            on_change=process_input,
            placeholder="What is this video about?"
        )
    else:
        if is_openai_api_key_set():
            st.info("👆 Add a YouTube video above to start chatting!")
        else:
            st.warning("🔑 Please enter your OpenAI API key first.")

    st.divider()
    st.markdown("""
    ### How to use:
    1. Enter your OpenAI API key
    2. Paste a YouTube video URL
    3. Wait for the video to be processed
    4. Start asking questions about the video!
    
    **Note:** The video must have captions/transcripts available for this to work.
    """)
    st.markdown("Source code: [Github](https://github.com/Anil-matcha/Chat-Youtube)")


if __name__ == "__main__":
    main()