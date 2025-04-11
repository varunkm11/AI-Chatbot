import os
import requests
import streamlit as st
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the API Key from environment variables
API_KEY = os.getenv("OPENROUTER_API_KEY")

# --- Streamlit App Setup ---
st.set_page_config(page_title="AI App Idea Generator", page_icon="💡")
st.title("💡 AI App Idea Generator")
st.write("Ask any question and get a response using OpenRouter's free AI models.")

# --- User Input Box ---
user_input = st.text_input("Enter your question:", "")

# --- When the button is clicked ---
if st.button("Get Response"):
    if user_input.strip() == "":
        st.warning("Please enter a question before submitting.")
    else:
        with st.spinner("Thinking..."):
            # API setup
            headers = {
                "Authorization": f"Bearer {API_KEY}"
            }

            data = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": [{"role": "user", "content": user_input}],
            }

            # Send request
            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

            # Handle response
            if response.status_code == 200:
                result = response.json()
                if 'choices' in result:
                    st.success(result['choices'][0]['message']['content'])
                else:
                    st.error("Unexpected response format. Try again.")
            else:
                st.error(f"API Error {response.status_code}: {response.json()}")
