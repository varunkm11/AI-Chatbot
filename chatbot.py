import requests
import streamlit as st

# --- Get API Key from Streamlit Secrets ---
API_KEY = st.secrets["OPENROUTER_API_KEY"]

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
            headers = {
                "Authorization": f"Bearer {API_KEY}"
            }

            data = {
                "model": "mistralai/mistral-7b-instruct",
                "messages": [{"role": "user", "content": user_input}],
            }

            response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=data)

            if response.status_code == 200:
                result = response.json()
                if 'choices' in result:
                    st.success(result['choices'][0]['message']['content'])
                else:
                    st.error("Unexpected response format. Try again.")
            else:
                st.error(f"API Error {response.status_code}: {response.json()}")
