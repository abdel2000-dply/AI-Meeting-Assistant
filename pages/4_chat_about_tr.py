import streamlit as st
from cohereAPI import chat_with_cohere

st.title("💬 Chat About Your Meeting")
st.subheader("Ask questions about your meeting transcript")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Display the transcript if available
if "transcript" in st.session_state and st.session_state.transcript:
    st.text_area("Meeting Transcript", st.session_state.transcript, height=200, max_chars=None)

    # User input for chat
    user_input = st.text_input("Ask a question about your meeting")

    if st.button("Send"):
        if user_input:
            context = {
                "transcript": st.session_state.transcript,
                "chat_history": st.session_state.chat_history
            }
            response = chat_with_cohere(user_input, context)
            if response:
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({"role": "chatbot", "content": response})
                st.success("Response generated successfully.")
            else:
                st.error("Failed to generate response.")

    # Display chat history
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.text_area("You", entry["content"], height=100, key=f"user_{entry['content']}")
        else:
            st.text_area("Chatbot", entry["content"], height=100, key=f"chatbot_{entry['content']}")
else:
    st.info("No transcription results available. Please upload or record audio first.")