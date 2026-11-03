
import os
import streamlit as st
from dotenv import load_dotenv
from google import genai

# Load API key from .env
load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

# Page configuration
st.set_page_config(
    page_title="My AI Chatbot",
    page_icon="🤖"
)

st.title("🤖 My AI Chatbot")
st.caption("Ask me anything! Powered by Google Gemini.")

# Check API key
if not API_KEY:
    st.error("Gemini API key not found. Please check your .env file.")
    st.stop()

# Connect to Gemini
client = genai.Client(api_key=API_KEY)

# Store conversation history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat input
user_input = st.chat_input("Type your question here...")

if user_input:
    # Display user message
    st.session_state.messages.append({
        "role": "user",
        "content": user_input
    })

    with st.chat_message("user"):
        st.markdown(user_input)

    # Generate AI response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            try:
                conversation = []

                for msg in st.session_state.messages:
                    role = "model" if msg["role"] == "assistant" else "user"
                    conversation.append({
                        "role": role,
                        "parts": [{"text": msg["content"]}]
                    })

                response = client.models.generate_content(
                    model="gemini-3.8-flash",
                    contents=conversation
                )

                answer = response.text or "I couldn't generate a response."
                st.markdown(answer)

                st.session_state.messages.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception as e:
                    error_message = str(e)

                    if "429" in error_message or "RESOURCE_EXHAUSTED" in error_message:
                                st.warning(
                                    "Daily Gemini API quota exceeded. "
                                    "Please try again after your quota resets."
                                )
                    elif "503" in error_message or "UNAVAILABLE" in error_message:
                            st.warning(
                                    "Gemini is temporarily busy. Please try again later."
                                )
                    else:
                     st.error(f"Something went wrong: {error_message}")
