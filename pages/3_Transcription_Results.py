import streamlit as st
from cohereAPI import summarize_darija, generate_dareja_todos

st.title("📄 Transcription Results")
st.subheader("View and download transcription results")

# Display the transcript if available
if "transcript" in st.session_state and st.session_state.transcript:
    st.text_area("Meeting Summary", st.session_state.transcript, height=200)
    st.download_button(
        label="Download Summary",
        data=st.session_state.transcript,
        file_name="meeting_summary.txt",
        mime="text/plain"
    )

    # Summarize the transcript using Cohere API
    if st.button("Summarize Transcript"):
        st.info("Summarizing the transcript...")
        summary = summarize_darija(st.session_state.transcript)
        if summary:
            st.text_area("Summary", summary, height=200)
        else:
            st.error("Failed to generate summary.")

    # Generate to-dos from the transcript using Cohere API
    if st.button("Generate To-Dos"):
        st.info("Generating to-dos from the transcript...")
        todos = generate_dareja_todos(st.session_state.transcript)
        if todos:
            st.text_area("To-Dos", todos, height=200)
        else:
            st.error("Failed to generate to-dos.")
else:
    st.info("No transcription results available. Please upload or record audio first.")
