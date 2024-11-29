import logging
from pathlib import Path
from pydub import AudioSegment

def save_uploaded_file(uploaded_file, filename):
    temp_file_path = Path(filename)
    with open(temp_file_path, "wb") as f:
        f.write(uploaded_file.getbuffer())
    logging.info(f"File saved: {temp_file_path}")
    return temp_file_path

def convert_mp3_to_wav(mp3_path):
    wav_output_path = mp3_path.with_suffix('.wav')
    audio = AudioSegment.from_mp3(mp3_path)
    audio.export(wav_output_path, format="wav")
    logging.info(f"Converted MP3 to WAV: {wav_output_path}")
    return wav_output_path
