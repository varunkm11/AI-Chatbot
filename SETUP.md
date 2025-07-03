# 🤖 Advanced AI Chatbot - Setup Guide

## Overview
This advanced chatbot system provides multiple deployment options and can be easily embedded into any website. It supports multiple AI models, real-time chat, conversation history, and customizable themes.

## Features
- ✅ Multiple AI models (Mistral, GPT-3.5, Claude, etc.)
- ✅ Real-time chat with WebSocket support
- ✅ Conversation history and memory
- ✅ Customizable themes (light/dark)
- ✅ Mobile responsive design
- ✅ Easy website integration
- ✅ Export chat history
- ✅ Multiple backend options (FastAPI, Flask, Streamlit)

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Set Up Environment Variables
Copy `.env.example` to `.env` and configure:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
HOST=0.0.0.0
PORT=8000
DEBUG=True
```

### 3. Choose Your Backend

#### Option A: FastAPI (Recommended for production)
```bash
python fastapi_chatbot.py
```
- High performance with async support
- WebSocket support for real-time chat
- Automatic API documentation at `/docs`
- Best for production deployments

#### Option B: Flask (Simple and lightweight)
```bash
python flask_chatbot.py
```
- Simple REST API
- Easy to understand and modify
- Good for quick prototypes

#### Option C: Streamlit (Interactive web app)
```bash
streamlit run advanced_chatbot.py
```
- Rich interactive interface
- Built-in configuration options
- Great for demos and internal use

### 4. Test the API
Visit `http://localhost:8000/web` (FastAPI) or `http://localhost:5000/web` (Flask) to test the web interface.

## Website Integration

### Method 1: Auto-Initialize with Data Attributes
Add this to your HTML:
```html
<script src="https://your-domain.com/static/chatbot-widget.js"></script>
<div data-chatbot 
     data-api-url="http://localhost:8000"
     data-position="bottom-right"
     data-theme="light"
     data-model="mistralai/mistral-7b-instruct"
     data-title="AI Assistant"
     data-placeholder="Type your message...">
</div>
```

### Method 2: Manual Initialization
```html
<script src="https://your-domain.com/static/chatbot-widget.js"></script>
<script>
const chatbot = new ChatbotWidget({
    apiUrl: 'http://localhost:8000',
    position: 'bottom-right',
    theme: 'light',
    model: 'mistralai/mistral-7b-instruct',
    title: 'AI Assistant',
    placeholder: 'Type your message...'
});
</script>
```

## Configuration Options

### Widget Options
- `apiUrl`: Backend API URL
- `position`: 'bottom-right', 'bottom-left', 'top-right', 'top-left'
- `theme`: 'light', 'dark'
- `model`: AI model to use
- `title`: Widget title
- `placeholder`: Input placeholder text

### Available AI Models
- `mistralai/mistral-7b-instruct` (Default, fast and free)
- `openai/gpt-3.5-turbo` (OpenAI GPT-3.5)
- `anthropic/claude-3-haiku` (Anthropic Claude)
- `google/gemma-7b-it` (Google Gemma)
- `meta-llama/llama-3-8b-instruct` (Meta Llama)

## API Endpoints

### FastAPI/Flask Common Endpoints
- `GET /` - API information
- `GET /api/models` - Get available models
- `POST /api/chat` - Send chat message
- `GET /api/conversations` - List conversations
- `GET /api/conversations/{id}` - Get conversation
- `DELETE /api/conversations/{id}` - Delete conversation
- `GET /health` - Health check
- `GET /web` - Web interface

### FastAPI Specific
- `WS /ws/{conversation_id}` - WebSocket endpoint
- `GET /docs` - API documentation

## Development Setup

### 1. Clone and Install
```bash
git clone <repository>
cd AI-Chatbot
pip install -r requirements.txt
```

### 2. Environment Setup
```bash
cp .env.example .env
# Edit .env with your API keys
```

### 3. Run Development Server
```bash
# FastAPI with auto-reload
uvicorn fastapi_chatbot:app --reload --host 0.0.0.0 --port 8000

# Flask with debug mode
python flask_chatbot.py

# Streamlit with auto-reload
streamlit run advanced_chatbot.py
```

## Production Deployment

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

### Nginx Configuration
```nginx
server {
    listen 80;
    server_name your-domain.com;
    
    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
    
    location /ws {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}
```

### Environment Variables for Production
```env
OPENROUTER_API_KEY=your_production_key
HOST=0.0.0.0
PORT=8000
DEBUG=False
CORS_ORIGINS=https://your-domain.com
DATABASE_URL=postgresql://user:pass@localhost/chatbot
REDIS_URL=redis://localhost:6379
```

## Customization

### Custom Styling
Modify the CSS in `static/chatbot-widget.js` to match your brand:
```css
.chatbot-toggle {
    background: linear-gradient(135deg, #your-color1, #your-color2);
}

.chatbot-header {
    background: linear-gradient(135deg, #your-color1, #your-color2);
}
```

### Custom System Prompts
Configure different AI personalities:
```javascript
const chatbot = new ChatbotWidget({
    apiUrl: 'http://localhost:8000',
    systemPrompt: 'You are a helpful customer service assistant for our e-commerce store.',
    // ... other options
});
```

## Monitoring and Analytics

### Health Check
```bash
curl http://localhost:8000/health
```

### Conversation Analytics
```bash
curl http://localhost:8000/api/conversations
```

## Troubleshooting

### Common Issues

1. **API Key Error**
   - Make sure your OpenRouter API key is valid
   - Check that the key is properly set in environment variables

2. **CORS Issues**
   - Configure CORS origins in your backend
   - Ensure the widget is loaded from an allowed domain

3. **WebSocket Connection Failed**
   - Check that WebSocket endpoint is accessible
   - Verify firewall and proxy settings

4. **Model Not Available**
   - Verify the model name is correct
   - Check your OpenRouter account limits

### Debug Mode
Enable debug logging:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

## Support

For issues and feature requests, please check:
1. Environment variables are correctly set
2. API keys are valid
3. Network connectivity to OpenRouter API
4. Browser console for JavaScript errors

## License

This project is open source and available under the MIT License.

---

## Advanced Features

### Database Integration
For production use, consider integrating with a database:
```python
# Example with SQLAlchemy
from sqlalchemy import create_engine, Column, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()

class Conversation(Base):
    __tablename__ = 'conversations'
    id = Column(String, primary_key=True)
    messages = Column(Text)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
```

### Redis for Session Management
```python
import redis
r = redis.Redis(host='localhost', port=6379, db=0)

# Store conversation in Redis
r.setex(f"conversation:{conversation_id}", 3600, json.dumps(messages))
```

### Rate Limiting
```python
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/chat")
@limiter.limit("10/minute")
async def chat(request: Request, message: ChatMessage):
    # ... chat logic
```

This setup provides a complete, production-ready AI chatbot system that can be easily integrated into any website!
