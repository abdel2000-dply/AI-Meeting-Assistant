import streamlit as st

st.title("AI Meeting Assistant")
st.subheader("Summarizing meetings, effortlessly!")

# File upload
uploaded_file = st.file_uploader("Upload your meeting audio", type=["mp3", "wav"])

if uploaded_file:
    st.info("Processing the audio...")
    # Mock API integration
    st.success("Transcription and summary ready!")
    summary = "This is a mock summary of the meeting discussion in Darija."
    st.text_area("Meeting Summary", summary, height=200)

    # Export summary
    st.download_button(
        label="Download Summary",
        data=summary,
        file_name="meeting_summary.txt",
        mime="text/plain"
    )
