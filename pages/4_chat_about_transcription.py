import streamlit as st
from cohereAPI import chat_with_cohere
import warnings

# Suppress the specific deprecation warning for st.experimental_set_query_params
warnings.filterwarnings("ignore", category=DeprecationWarning, message="st.experimental_set_query_params")

st.title("💬 Chat About Your Meeting")
st.subheader("Ask questions about your meeting transcript")

# Initialize session state for chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# Function to display chat history with bubbles
def display_chat_history():
    for entry in st.session_state.chat_history:
        with st.chat_message(entry["role"]):
            st.markdown(entry["content"])

# Display the transcript if available
if "transcript" in st.session_state and st.session_state.transcript:
    st.text_area("Meeting Transcript", st.session_state.transcript, height=200, max_chars=None)

    # User input for chat
    user_input = st.chat_input("Ask a question about your meeting")

    if user_input:
        context = {
            "transcript": st.session_state.transcript,
            "chat_history": st.session_state.chat_history,
            "language_sign": st.session_state.language_sign
        }
        
        response = chat_with_cohere(user_input, context, st.session_state.language_sign)

        if response:
            # Add user input and chatbot response to history
            st.session_state.chat_history.append({"role": "user", "content": user_input})
            st.session_state.chat_history.append({"role": "assistant", "content": response})
            st.success("Response generated successfully.")
        else:
            st.error("Failed to generate response.")

    # Display chat history with new bubble layout
    display_chat_history()

    # Option to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.chat_history.clear()

else:
    st.info("No transcription results available. Please upload or record audio first.")
