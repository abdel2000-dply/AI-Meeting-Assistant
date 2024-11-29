import streamlit as st
from pathlib import Path
from utils.transcription import transcribe_file
import logging

st.title("🎙️ Record Audio")
st.subheader("Record a voice message for transcription")

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""

# Audio recording
audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)
    temp_recorded_audio_path = Path("temp_recorded_audio.wav")
    with open(temp_recorded_audio_path, "wb") as f:
        f.write(audio_value.getbuffer())
    logging.info(f"Saved recorded audio: {temp_recorded_audio_path}")

    # Select the language before starting processing
    language_sign = st.selectbox("Select the language for transcription", ["EN", "AR", "FR"])

    # Add a button to start processing the recorded audio
    if st.button("Transcribe Recorded Audio"):
        st.info("Processing the recorded audio...")
        logging.info("Processing the recorded audio...")
        # Transcribe the recorded audio
        transcript_path = transcribe_file(temp_recorded_audio_path, language_sign)

        if transcript_path and transcript_path.exists():
            with open(transcript_path, "r") as f:
                st.session_state.transcript = f.read()
            st.success("Transcription completed.")
        else:
            st.error("Transcription failed. Please check the logs for more details.")
            logging.error("Transcription failed. Please check the logs for more details.")
