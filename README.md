# AI Meeting Assistant

AI Meeting Assistant is a Streamlit-based web application that allows users to upload or record audio from meetings, transcribe the audio using Wit.ai, and generate summaries and to-do lists using the Cohere API. The application supports multiple languages, including English, Arabic, and French.

## Features

- **Upload Audio**: Upload audio files (MP3 or WAV) for transcription.
- **Record Audio**: Record audio directly from the browser for transcription.
- **Transcription**: Transcribe audio files using Wit.ai.
- **Summarization**: Summarize transcribed text using the Cohere API.
- **To-Do List Generation**: Generate to-do lists from transcribed text using the Cohere API.
- **Multi-Language Support**: Supports English, Arabic, and French.

## Installation

1. **Clone the repository**:
  ```sh
  git clone https://github.com/yourusername/AI-Meeting-Assistant.git
  cd AI-Meeting-Assistant
  ```

2. **Create a virtual environment**:
  ```sh
  python -m venv venv
  source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
  ```

3. **Install the dependencies**:
  ```sh
  pip install -r requirements.txt
  ```

4. **Set up environment variables**:
  Create a `.env` file in the root directory and add your API keys:
  ```env
  WIT_API_KEY_ENGLISH=your_wit_api_key_for_english
  WIT_API_KEY_ARABIC=your_wit_api_key_for_arabic
  WIT_API_KEY_FRENCH=your_wit_api_key_for_french
  COHERE_API_KEY=your_cohere_api_key
  ```

## Usage

1. **Run the Streamlit app**:
  ```sh
  streamlit run app.py
  ```

2. **Navigate through the app**:
  - **Upload Audio**: Go to the "Upload Audio" page to upload an audio file for transcription.
  - **Record Audio**: Go to the "Record Audio" page to record audio directly from your browser.
  - **Transcription Results**: View and download transcription results, generate summaries, and create to-do lists.

## Project Structure
```
├── app.py
├── pages/
│   ├── 1_Upload_Audio.py
│   ├── 2_Record_Audio.py
│   └── 3_Transcription_Results.py
├── utils/
│   ├── __init__.py
│   ├── audio_processing.py
│   └── transcription.py
├── cohereAPI.py
├── .env
├── requirements.txt
└── README.md
```

- **app.py**: Main entry point for the Streamlit app.
- **pages/**: Contains the different pages of the app.
  - **1_Upload_Audio.py**: Handles audio file uploads.
  - **2_Record_Audio.py**: Handles audio recording.
  - **3_Transcription_Results.py**: Displays transcription results and integrates with the Cohere API.
- **utils/**: Contains utility functions for audio processing and transcription.
  - **audio_processing.py**: Functions for saving and converting audio files.
  - **transcription.py**: Functions for transcribing audio using Wit.ai.
- **cohereAPI.py**: Functions for summarizing text and generating to-do lists using the Cohere API.
- **.env**: Environment variables file (not included in the repository).
- **requirements.txt**: List of dependencies.
- **README.md**: Project documentation.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.
