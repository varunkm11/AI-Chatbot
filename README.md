# 💡 AI App Idea Generator

This is a simple but powerful AI-based Streamlit app that generates creative responses to your questions using OpenRouter's free AI models (like Mistral-7B).

---

## 🚀 Demo

🔗 [Live Demo Link](https://ai-chatbot-8u7uwybdb7evgsrw7yxvat.streamlit.app/)  

---
## 🧠 Features

- Interactive and lightweight UI built with Streamlit.
- Uses OpenRouter API to access powerful open-source LLMs like Mistral 7B.
- Fast responses and easy to use.
- Secure API key usage via `st.secrets`.

---

## 🛠️ Installation

### 1. Clone this repository
```bash
git clone https://github.com/your-username/ai-app-idea-generator.git
cd ai-app-idea-generator
```
### 2. Create and activate a virtual environment (optional but recommended)
```bash
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```
### 3. Install dependencies
```bash
pip install -r requirements.txt
```
### 🔐 API Key Setup
``` bash
To keep your API key secure, use Streamlit Secrets:
Create a .streamlit/secrets.toml file.
Add the following:
OPENROUTER_API_KEY = "your_openrouter_api_key_here"
```
### 💻 Run the App Locally
``` bash
streamlit run app.py
```
### 📄 File Structure
```bash
📁 ai-app-idea-generator/
├── app.py
├── requirements.txt
└── .streamlit/
    └── secrets.toml
```
### 🤝 Contributing
Pull requests are welcome! If you'd like to improve features, fix bugs, or add enhancements, feel free to open a PR. Please follow standard best practices in coding and documentation.

### 🌟 Support
If you find this project helpful, feel free to give it a ⭐ on GitHub and share it with others!
