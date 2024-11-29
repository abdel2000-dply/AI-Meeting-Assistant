import logging
import os
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv
from collections import deque
from tafrigh import Config, TranscriptType, farrigh
from pydub import AudioSegment

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables from .env file
load_dotenv()

# Define Wit.ai API keys for languages using environment variables
LANGUAGE_API_KEYS = {
    'EN': os.getenv('WIT_API_KEY_ENGLISH'),
    'AR': os.getenv('WIT_API_KEY_ARABIC'),
    'FR': os.getenv('WIT_API_KEY_FRENCH'),
}

# Check if at least one API key is provided
if not any(LANGUAGE_API_KEYS.values()):
    st.error("Error: At least one Wit.ai API key must be provided in the .env file.")
    st.stop()

def convert_mp3_to_wav(mp3_path):
    wav_output_path = mp3_path.with_suffix('.wav')
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_output_path, format="wav")
    logging.info(f"Converted MP3 to WAV: {wav_output_path}")
    return wav_output_path

def transcribe_file(file_path, language_sign):
    wit_api_key = LANGUAGE_API_KEYS.get(language_sign.upper())
    if not wit_api_key:
        st.error(f"API key not found for language: {language_sign}")
        logging.error(f"API key not found for language: {language_sign}")
        return None

    # Convert MP3 to WAV
    if file_path.suffix == '.mp3':
        file_path = convert_mp3_to_wav(file_path)

    config = Config(
        urls_or_paths=[str(file_path)],
        skip_if_output_exist=False,
        playlist_items="",
        verbose=False,
        model_name_or_path="",
        task="",
        language="",
        use_faster_whisper=False,
        beam_size=0,
        ct2_compute_type="",
        wit_client_access_tokens=[wit_api_key],
        max_cutting_duration=5,
        min_words_per_segment=1,
        save_files_before_compact=False,
        save_yt_dlp_responses=False,
        output_sample=0,
        output_formats=[TranscriptType.TXT, TranscriptType.SRT],
        output_dir=str(file_path.parent),
    )

    logging.info(f"Transcribing file: {file_path}")
    try:
        progress = deque(farrigh(config), maxlen=0)
        logging.info("Transcription completed. Check the output directory for the generated files.")
        return file_path.with_suffix('.txt')
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        st.error(f"Error during transcription: {e}")
        return None

st.title("AI Meeting Assistant")
st.subheader("Summarizing meetings, effortlessly!")

# Initialize session state
if 'transcript' not in st.session_state:
    st.session_state.transcript = ""

# File upload
uploaded_file = st.file_uploader("Upload your meeting audio", type=["mp3", "wav"])

if uploaded_file:
    st.info("File uploaded successfully.")
    # Save the uploaded file to a temporary location
    temp_file_path = Path("temp_audio_file.mp3")
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    logging.info(f"Saved uploaded file: {temp_file_path}")

    st.success("File saved successfully. Ready to process.")
    
    # Select the language before starting processing
    language_sign = st.selectbox("Select the language", options=["EN", "AR", "FR"])
    
    # Add a button to start processing
    if st.button("Start Processing"):
        st.info("Processing the audio...")
        logging.info("Processing the audio...")
        # Transcribe the uploaded file
        transcript_path = transcribe_file(temp_file_path, language_sign)
        if transcript_path:
            with open(transcript_path, "r") as f:
                st.session_state.transcript = f.read()
            st.success("Transcription completed.")
        else:
            st.error("Transcription failed. Please check the logs for more details.")
            logging.error("Transcription failed. Please check the logs for more details.")

# Display the transcript if available
if st.session_state.transcript:
    st.text_area("Meeting Summary", st.session_state.transcript, height=200)
    st.download_button(
        label="Download Summary",
        data=st.session_state.transcript,
        file_name="meeting_summary.txt",
        mime="text/plain"
    )

# Audio recording
audio_value = st.audio_input("Record a voice message")

if audio_value:
    st.audio(audio_value)
    # Save the recorded audio to a temporary file
    temp_recorded_audio_path = Path("temp_recorded_audio.wav")
    with open(temp_recorded_audio_path, "wb") as f:
        f.write(audio_value.getbuffer())
    logging.info(f"Saved recorded audio: {temp_recorded_audio_path}")

    # Select the language before starting processing
    language_sign = st.selectbox("Select the language for recorded audio", options=["EN", "AR", "FR"])

    # Add a button to start processing the recorded audio
    if st.button("Start Processing Recorded Audio"):
        st.info("Processing the recorded audio...")
        logging.info("Processing the recorded audio...")
        # Transcribe the recorded audio
        recorded_transcript_path = transcribe_file(temp_recorded_audio_path, language_sign)
        if recorded_transcript_path:
            with open(recorded_transcript_path, "r") as f:
                st.session_state.transcript = f.read()
            st.success("Recorded audio transcription completed.")
        else:
            st.error("Recorded audio transcription failed. Please check the logs for more details.")
            logging.error("Recorded audio transcription failed. Please check the logs for more details.")
