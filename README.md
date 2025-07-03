# 💡 # 🤖 Advanced AI Chatbot

A comprehensive AI chatbot system with multiple deployment options, advanced features, and easy website integration.

## 🚀 Features

### ✨ Advanced Chatbot Capabilities
- **Multiple AI Models**: Support for Mistral, GPT-3.5, Claude, Gemma, and Llama
- **Conversation Memory**: Maintains context across messages
- **Real-time Chat**: WebSocket support for instant responses
- **Typing Indicators**: Shows when AI is thinking
- **Export Chat History**: Download conversations as JSON
- **System Prompts**: Customize AI behavior and personality

### 🎨 Rich User Interface
- **Modern Design**: Beautiful gradient backgrounds and animations
- **Dark Mode**: Built-in theme switching
- **Mobile Responsive**: Works on all devices
- **Customizable**: Easy to modify colors, positioning, and styling
- **Chat Statistics**: Track conversation metrics

### 🌐 Multiple Deployment Options
- **Streamlit App**: Rich interactive interface with sidebar controls
- **FastAPI Backend**: High-performance async API with WebSocket support
- **Flask Backend**: Simple REST API for basic integration
- **JavaScript Widget**: Embeddable chatbot for any website

### 🔧 Easy Integration
- **Simple Embedding**: Just add a script tag and data attributes
- **API Access**: RESTful endpoints for programmatic access
- **Widget Customization**: Configure position, theme, and behavior
- **CORS Support**: Works with any domain

## 📦 Installation

### Quick Setup
```bash
# Clone the repository
git clone <repository-url>
cd AI-Chatbot

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env with your OpenRouter API key
```

### Environment Configuration
Edit `.env` file:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

## 🏃 Running the Applications

### Option 1: Streamlit App (Recommended for demos)
```bash
streamlit run advanced_chatbot.py
```
- Visit: http://localhost:8501
- Features: Rich UI, model selection, system prompts, chat export

### Option 2: FastAPI Backend (Recommended for production)
```bash
python fastapi_chatbot.py
```
- Visit: http://localhost:8000/web
- API Docs: http://localhost:8000/docs
- Features: WebSocket support, high performance, auto-documentation

### Option 3: Flask Backend (Simple REST API)
```bash
python flask_chatbot.py
```
- Visit: http://localhost:5000/web
- Features: Simple REST API, easy to understand

## 🌐 Website Integration

### Method 1: Auto-Initialize (Easiest)
Add to your HTML:
```html
<script src="https://your-domain.com/static/chatbot-widget.js"></script>
<div data-chatbot 
     data-api-url="http://localhost:8000"
     data-position="bottom-right"
     data-theme="light"
     data-title="AI Assistant">
</div>
```

### Method 2: Manual Initialization (More Control)
```html
<script src="https://your-domain.com/static/chatbot-widget.js"></script>
<script>
const chatbot = new ChatbotWidget({
    apiUrl: 'http://localhost:8000',
    position: 'bottom-right',
    theme: 'light',
    model: 'mistralai/mistral-7b-instruct',
    title: 'AI Assistant'
});
</script>
```

## 📱 Demo

Check out the demo page at `demo.html` to see the chatbot in action with example integrations.

## 🛠️ Configuration Options

### Widget Options
- `apiUrl`: Backend API URL
- `position`: 'bottom-right', 'bottom-left', 'top-right', 'top-left'
- `theme`: 'light', 'dark'
- `model`: AI model to use
- `title`: Widget title
- `placeholder`: Input placeholder text

### Available AI Models
- `mistralai/mistral-7b-instruct` - Fast and efficient (Default)
- `openai/gpt-3.5-turbo` - OpenAI GPT-3.5
- `anthropic/claude-3-haiku` - Anthropic Claude
- `google/gemma-7b-it` - Google Gemma
- `meta-llama/llama-3-8b-instruct` - Meta Llama

## 🔗 API Endpoints

### Common Endpoints (FastAPI & Flask)
- `POST /api/chat` - Send chat message
- `GET /api/models` - Get available models
- `GET /api/conversations` - List conversations
- `GET /api/conversations/{id}` - Get conversation
- `DELETE /api/conversations/{id}` - Delete conversation
- `GET /health` - Health check

### FastAPI Specific
- `WS /ws/{conversation_id}` - WebSocket endpoint
- `GET /docs` - Interactive API documentation

## 🎯 Use Cases

### Business Applications
- **Customer Support**: Automated customer service chatbot
- **E-commerce**: Product recommendations and order assistance
- **Education**: Interactive learning assistant
- **Healthcare**: Basic medical information and appointment scheduling

### Technical Applications
- **Code Assistant**: Programming help and debugging
- **Documentation**: Interactive documentation chatbot
- **API Testing**: Conversational API testing interface
- **Data Analysis**: Natural language data queries

## 📊 Features Comparison

| Feature | Streamlit | FastAPI | Flask | Widget |
|---------|-----------|---------|--------|--------|
| Real-time Chat | ✅ | ✅ | ❌ | ✅ |
| WebSocket | ❌ | ✅ | ❌ | ✅ |
| API Documentation | ❌ | ✅ | ❌ | ❌ |
| Rich UI | ✅ | ✅ | ✅ | ✅ |
| Easy Deployment | ✅ | ✅ | ✅ | ✅ |
| Production Ready | ⚠️ | ✅ | ✅ | ✅ |

## 🔧 Development

### Project Structure
```
AI-Chatbot/
├── advanced_chatbot.py      # Streamlit app
├── fastapi_chatbot.py       # FastAPI backend
├── flask_chatbot.py         # Flask backend
├── static/
│   └── chatbot-widget.js    # JavaScript widget
├── demo.html                # Demo page
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
└── README.md               # This file
```

### Adding New Features
1. **New AI Models**: Add to the `MODELS` dictionary
2. **Custom Themes**: Modify CSS in the widget
3. **Additional Endpoints**: Add to the FastAPI/Flask apps
4. **UI Enhancements**: Update the Streamlit or HTML interfaces

## 🚀 Deployment

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8000
CMD ["uvicorn", "fastapi_chatbot:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Production Considerations
- Use environment variables for API keys
- Set up proper CORS origins
- Use a reverse proxy (Nginx)
- Enable SSL/TLS
- Monitor API usage and rate limits

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 💡 Tips

- **API Keys**: Get your OpenRouter API key from https://openrouter.ai/
- **Rate Limits**: Be aware of API rate limits for your chosen models
- **Customization**: The widget CSS can be easily customized for your brand
- **Testing**: Use the demo page to test different configurations

## 📞 Support

For questions and support:
1. Check the demo page for examples
2. Review the API documentation
3. Test with the included examples
4. Check browser console for errors

---

**Made with ❤️ for the AI community**

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
