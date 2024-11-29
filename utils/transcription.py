# utils/transcription.py

import logging
import os
from tafrigh import Config, farrigh, TranscriptType
from pathlib import Path
from collections import deque
from utils.audio_processing import convert_mp3_to_wav
from dotenv import load_dotenv
from pydub import AudioSegment

# Load environment variables from .env file
load_dotenv()

LANGUAGE_API_KEYS = {
    'EN': os.getenv('WIT_API_KEY_ENGLISH'),
    'AR': os.getenv('WIT_API_KEY_ARABIC'),
    'FR': os.getenv('WIT_API_KEY_FRENCH'),
}

def transcribe_file(file_path, language_sign):
    logging.info(f"Starting transcription for file: {file_path} with language: {language_sign}")
    
    wit_api_key = LANGUAGE_API_KEYS.get(language_sign.upper())
    if not wit_api_key:
        logging.error(f"API key not found for language: {language_sign}")
        raise ValueError(f"API key not found for language: {language_sign}")

    # Convert MP3 to WAV if the file is an MP3
    if file_path.suffix == '.mp3':
        logging.info(f"Converting MP3 to WAV for file: {file_path}")
        file_path = convert_mp3_to_wav(file_path)

    # Initialize Config with all required arguments
    try:
        config = Config(
            urls_or_paths=[str(file_path)],  # Audio file path
            skip_if_output_exist=False,
            playlist_items="",
            verbose=False,
            model_name_or_path="",
            task="transcribe",  # You can change this to your task if needed
            language=language_sign.upper(),
            use_faster_whisper=False,
            beam_size=5,  # You can adjust the beam size if needed
            ct2_compute_type="auto",
            wit_client_access_tokens=[wit_api_key],
            max_cutting_duration=5,
            min_words_per_segment=1,
            save_files_before_compact=False,
            save_yt_dlp_responses=False,
            output_sample=0,
            output_formats=[TranscriptType.TXT, TranscriptType.SRT],
            output_dir=str(file_path.parent),  # Output directory for transcriptions
        )

        # Run the transcription process
        progress = deque(farrigh(config), maxlen=0)  # Using farrigh to transcribe
        logging.info("Transcription process completed successfully.")
        
        return file_path.with_suffix('.txt')  # Return the path to the generated transcript
    except Exception as e:
        logging.error(f"Error during transcription: {e}")
        return None