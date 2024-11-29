import streamlit as st

st.set_page_config(
    page_title="AI Meeting Assistant",
    page_icon="🎙️",
    layout="wide",
)

st.title("🎙️ AI Meeting Assistant")
st.subheader("Summarizing meetings effortlessly!")

st.markdown(
    """
    Welcome to the AI Meeting Assistant. Use the navigation menu to:
    - Upload audio files for transcription
    - Record audio directly
    - View and download transcription results.
    """
)
