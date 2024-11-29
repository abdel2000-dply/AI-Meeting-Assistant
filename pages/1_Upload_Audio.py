import streamlit as st
from pathlib import Path
import logging
from utils.audio_processing import save_uploaded_file
from utils.transcription import transcribe_file

st.title("📤 Upload Audio")
st.subheader("Upload your meeting audio file for transcription")

uploaded_file = st.file_uploader("Upload an audio file", type=["mp3", "wav"])

if uploaded_file:
    st.info("File uploaded successfully.")
    temp_file_path = save_uploaded_file(uploaded_file, "temp_audio_file.mp3")

    # Language selection
    language_sign = st.selectbox("Select the language", ["EN", "AR", "FR"])

    if st.button("Transcribe Audio"):
        st.info("Processing the audio...")
        transcript_path = transcribe_file(temp_file_path, language_sign)

        if transcript_path:
            with open(transcript_path, "r") as f:
                st.session_state.transcript = f.read()
            st.success("Transcription completed.")
        else:
            st.error("Transcription failed.")
