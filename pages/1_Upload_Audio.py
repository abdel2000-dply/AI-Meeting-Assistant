import streamlit as st
from pathlib import Path
import logging

# Lazy load the transcription function
@st.cache_resource
def load_transcription_module():
    from utils.transcription import transcribe_file
    return transcribe_file

transcribe_file = load_transcription_module()

st.title("📤 Upload Audio")
st.subheader("Upload your meeting audio file for transcription")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

if uploaded_file:
    st.info("File uploaded successfully.")
    temp_file_path = Path("temp_audio_file.mp3")
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    logging.info(f"Saved uploaded file: {temp_file_path}")

    # Language selection
    language_sign = st.selectbox("Select the language", ["EN", "AR", "FR"])

    if st.button("Transcribe Audio"):
        st.info("Processing the audio...")
        transcript_path = transcribe_file(temp_file_path, language_sign, output_file_name="transcript.txt")

        if transcript_path:
            with open(transcript_path, "r") as f:
                st.session_state.transcript = f.read()
            st.session_state.language_sign = language_sign  # Save the language in session state
            st.success("Transcription completed.")
        else:
            st.error("Transcription failed.")
