import streamlit as st
from cohereAPI import summarize_text, generate_todos

st.title("📄 Transcription Results")
st.subheader("View and download transcription results")

# Initialize session state for summary and to-dos
if "summary" not in st.session_state:
    st.session_state.summary = ""
if "todos" not in st.session_state:
    st.session_state.todos = ""

# Display the transcript if available
if "transcript" in st.session_state and st.session_state.transcript:
    st.text_area("Meeting Transcript", st.session_state.transcript, height=200)
    st.download_button(
        label="Download Transcript",
        data=st.session_state.transcript,
        file_name="meeting_transcript.txt",
        mime="text/plain"
    )

    # Summarize the transcript using Cohere API
    if st.button("Summarize Transcript"):
        st.info("Summarizing the transcript...")
        summary = summarize_text(st.session_state.transcript, st.session_state.language_sign)
        if summary:
            st.session_state.summary = summary
            st.success("Summary generated successfully.")
        else:
            st.error("Failed to generate summary.")

    # Generate to-dos from the transcript using Cohere API
    if st.button("Generate To-Dos"):
        st.info("Generating to-dos from the transcript...")
        todos = generate_todos(st.session_state.transcript, st.session_state.language_sign)
        if todos:
            st.session_state.todos = todos
            st.success("To-Dos generated successfully.")
        else:
            st.error("Failed to generate to-dos.")

    # Display the summary if available
    if st.session_state.summary:
        st.text_area("Summary", st.session_state.summary, height=200)

    # Display the to-dos if available
    if st.session_state.todos:
        st.text_area("To-Dos", st.session_state.todos, height=200)
else:
    st.info("No transcription results available. Please upload or record audio first.")
