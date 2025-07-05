# Roseew - AI Assistant with Real-Time Capabilities

A modern AI chatbot named Roseew, built with Python Flask and OpenRouter API, featuring a beautiful ChatGPT-like interface with real-time data capabilities. The application is ready for Heroku deployment.

## Features

- 🤖 **AI-powered conversations** using OpenRouter API
- 🕒 **Real-time data access** with current date/time context
- 💬 **ChatGPT-inspired UI** with dark theme (black & gray)
- 📱 **Responsive design** that works on all devices
- 🔄 **Conversation memory** maintains context within sessions
- ⚡ **Fast and lightweight** Flask backend
- 🚀 **Heroku-ready deployment** configuration

## Screenshots

The interface features:
- Clean, minimalist design with black and gray color scheme
- Sidebar for chat history and new chat creation
- Real-time typing indicators
- Message timestamps
- Smooth animations and transitions
- Mobile-responsive layout

## Tech Stack

- **Backend**: Python Flask
- **AI API**: OpenRouter (supports multiple AI models)
- **Frontend**: HTML5, CSS3, JavaScript (Vanilla)
- **Deployment**: Heroku
- **Styling**: Custom CSS with ChatGPT-inspired design

## Setup Instructions

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd AI-Chatbot
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Environment Configuration

1. Copy the example environment file:
```bash
copy .env.example .env
```

2. Edit `.env` and add your API keys:
```env
OPENROUTER_API_KEY=your_openrouter_api_key_here
SECRET_KEY=your_secret_key_here
```

### 4. Get OpenRouter API Key

1. Visit [OpenRouter.ai](https://openrouter.ai/)
2. Create an account and get your API key
3. Add the key to your `.env` file

### 5. Run Locally

```bash
python app.py
```

The application will be available at `http://localhost:5000`

## Heroku Deployment

### Prerequisites

1. Install [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli)
2. Create a Heroku account

### Deployment Steps

1. **Login to Heroku**:
```bash
heroku login
```

2. **Create Heroku App**:
```bash
heroku create your-chatbot-name
```

3. **Set Environment Variables**:
```bash
heroku config:set OPENROUTER_API_KEY=your_openrouter_api_key_here
heroku config:set SECRET_KEY=your_secret_key_here
```

4. **Deploy**:
```bash
git add .
git commit -m "Initial deployment"
git push heroku main
```

5. **Open App**:
```bash
heroku open
```

## Configuration

### AI Model Selection

The chatbot uses `anthropic/claude-3.5-sonnet` by default. You can change this in `app.py`:

```python
data = {
    "model": "anthropic/claude-3.5-sonnet",  # Change this model
    # Other available models:
    # "openai/gpt-4-turbo"
    # "openai/gpt-3.5-turbo"
    # "anthropic/claude-3-opus"
    # "google/gemini-pro"
    # And many more on OpenRouter
}
```

### Real-Time Features

The chatbot includes real-time context such as:
- Current date and time
- Day of the week
- Formatted timestamps

This information is automatically included in conversations to provide current context.

## API Endpoints

- `GET /` - Main chat interface
- `POST /chat` - Send message to AI
- `POST /new-chat` - Start new conversation
- `GET /health` - Health check endpoint

## File Structure

```
AI-Chatbot/
├── app.py                 # Main Flask application
├── templates/
│   └── index.html        # Chat interface
├── requirements.txt      # Python dependencies
├── Procfile             # Heroku process file
├── runtime.txt          # Python version for Heroku
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## Features in Detail

### Real-Time Capabilities
- Current date/time injection into conversations
- Context-aware responses based on current information
- Ability to answer time-sensitive queries

### UI/UX Features
- Dark theme with black (#0d1117) and gray (#161b22) colors
- Smooth animations and transitions
- Typing indicators while AI is processing
- Message timestamps
- Responsive design for mobile devices
- Sidebar for chat management

### Technical Features
- Session-based conversation memory
- Error handling and user feedback
- Health check endpoint for monitoring
- Environment-based configuration
- Production-ready logging

## Troubleshooting

### Common Issues

1. **API Key Not Working**:
   - Ensure your OpenRouter API key is valid
   - Check that the environment variable is set correctly

2. **Heroku Deployment Fails**:
   - Verify all files are committed to git
   - Check Heroku logs: `heroku logs --tail`
   - Ensure environment variables are set on Heroku

3. **Local Development Issues**:
   - Make sure all dependencies are installed
   - Check that `.env` file exists and has correct values
   - Verify Python version compatibility

### Debugging

Enable debug mode locally by modifying `app.py`:
```python
app.run(host='0.0.0.0', port=port, debug=True)  # Set debug=True
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## License

This project is open source and available under the MIT License.

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review Heroku logs for deployment issues
3. Ensure all environment variables are configured correctly

## Future Enhancements

Potential improvements:
- User authentication and chat history persistence
- File upload capabilities
- Voice message support
- Multiple AI model selection in UI
- Chat export functionality
- Custom theme options
