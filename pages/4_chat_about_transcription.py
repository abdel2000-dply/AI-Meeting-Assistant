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

# Initialize session state for typing indicator
if "is_typing" not in st.session_state:
    st.session_state.is_typing = False

# Function to display chat history with bubbles
def display_chat_history():
    for entry in st.session_state.chat_history:
        if entry["role"] == "user":
            st.markdown(f'<div style="text-align: left; background-color: #ADD8E6; color: black; padding: 10px; border-radius: 10px; max-width: 75%; margin-bottom: 5px; margin-left: 5px;">{entry["content"]}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div style="text-align: right; background-color: #D3D3D3; color: black; padding: 10px; border-radius: 10px; max-width: 75%; margin-bottom: 5px; margin-right: 5px;">{entry["content"]}</div>', unsafe_allow_html=True)

# Display the transcript if available
if "transcript" in st.session_state and st.session_state.transcript:
    st.text_area("Meeting Transcript", st.session_state.transcript, height=200, max_chars=None)

    # User input for chat
    user_input = st.text_input("Ask a question about your meeting", placeholder="Type your question here...")

    # Chat interaction and typing indicator
    if st.session_state.is_typing:
        st.text("Chatbot is typing...")

    if st.button("Send"):
        if user_input:
            # Set the typing indicator to True
            st.session_state.is_typing = True
            st.experimental_set_query_params(typing="true")

            context = {
                "transcript": st.session_state.transcript,
                "chat_history": st.session_state.chat_history,
                "language_sign": st.session_state.language_sign
            }
            
            response = chat_with_cohere(user_input, context, st.session_state.language_sign)

            if response:
                # Add user input and chatbot response to history
                st.session_state.chat_history.append({"role": "user", "content": user_input})
                st.session_state.chat_history.append({"role": "chatbot", "content": response})
                st.success("Response generated successfully.")
            else:
                st.error("Failed to generate response.")
                
            # Set typing indicator to False
            st.session_state.is_typing = False
            st.experimental_set_query_params(typing="false")

    # Display chat history with new bubble layout
    display_chat_history()

    # Option to clear chat history
    if st.button("Clear Chat History"):
        st.session_state.chat_history.clear()
        st.experimental_set_query_params(clear="true")

else:
    st.info("No transcription results available. Please upload or record audio first.")
