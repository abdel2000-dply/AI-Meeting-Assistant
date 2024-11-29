import streamlit as st

st.title("📄 Transcription Results")
st.subheader("View and download transcription results")

if "transcript" in st.session_state and st.session_state.transcript:
    st.text_area("Meeting Summary", st.session_state.transcript, height=300)
    st.download_button(
        "Download Summary",
        st.session_state.transcript,
        file_name="meeting_summary.txt",
        mime="text/plain",
    )
else:
    st.info("No transcription available yet. Upload or record an audio file first.")
