# Roseew - AI Assistant with Real-Time Capabilities

A modern AI chatbot named Roseew, built with Python Flask and OpenRouter API, featuring a beautiful ChatGPT-like interface with real-time data capabilities. Deployed on Vercel for fast and reliable performance.

## 🌟 Live Demo

**🚀 [Try Roseew Live](https://roseew-ai-chatbot.vercel.app/)**

Experience the chatbot in action! The live demo is deployed on Vercel and ready to use.

## Features

- 🤖 **AI-powered conversations** using OpenRouter API
- 🕒 **Real-time data access** with current date/time context
- 💬 **ChatGPT-inspired UI** with dark theme (black & gray)
- 📱 **Responsive design** that works on all devices
- 🔄 **Conversation memory** maintains context within sessions
- ⚡ **Fast and lightweight** Flask backend
- 🚀 **Vercel deployment ready** configuration

## 🔧 Quick Tech Overview

**Frontend**: HTML5 + CSS3 + Vanilla JavaScript | **Backend**: Python Flask | **AI**: OpenRouter API (Claude 3.5 Sonnet) | **Deployment**: Vercel

## Screenshots

The interface features:
- Clean, minimalist design with black and gray color scheme
- Sidebar for chat history and new chat creation
- Real-time typing indicators
- Message timestamps
- Smooth animations and transitions
- Mobile-responsive layout

## 🛠️ Tech Stack

### Frontend Technologies
- **HTML5** - Semantic markup and structure
- **CSS3** - Modern styling with:
  - Flexbox layout system
  - CSS Grid for responsive design
  - Custom animations and transitions
  - Dark theme with CSS variables
  - Webkit scrollbar customization
- **Vanilla JavaScript (ES6+)** - Interactive functionality:
  - Async/await for API calls
  - DOM manipulation
  - Real-time message handling
  - Auto-resizing textarea
  - Keyboard event handling
- **Font Awesome 6.4.0** - Professional icons and symbols
- **Responsive Design** - Mobile-first approach with media queries

### Backend Technologies
- **Python 3.11+** - Core programming language
- **Flask 2.3.3** - Lightweight web framework
- **Requests 2.31.0** - HTTP library for API calls
- **Python-dotenv 1.0.0** - Environment variable management
- **Gunicorn 21.2.0** - WSGI HTTP Server for deployment

### AI & External Services
- **OpenRouter API** - AI model access gateway
- **Anthropic Claude 3.5 Sonnet** - Primary AI model
- **Multiple AI Models Support**:
  - OpenAI GPT-4 Turbo
  - OpenAI GPT-3.5 Turbo
  - Anthropic Claude 3 Opus
  - Google Gemini Pro
  - And many more via OpenRouter

### Development & Deployment
- **Git** - Version control system
- **Vercel** - Primary deployment platform
- **Vercel CLI** - Deployment and management tools
- **Node.js & NPM** - Package management for deployment tools

### Architecture & Patterns
- **RESTful API Design** - Clean endpoint structure
- **Session Management** - Flask sessions for conversation state
- **Environment Configuration** - Secure API key management
- **MVC Pattern** - Separation of concerns
- **Real-time Communication** - AJAX for seamless user experience

### Security Features
- **Environment Variables** - Secure API key storage
- **CORS Handling** - Cross-origin request management
- **Input Validation** - Server-side request validation
- **Error Handling** - Comprehensive error management

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

## Vercel Deployment

### Prerequisites

1. Install [Vercel CLI](https://vercel.com/cli) globally:
```bash
npm i -g vercel
```

2. Create a Vercel account at [vercel.com](https://vercel.com)

### Deployment Steps

1. **Login to Vercel**:
```bash
vercel login
```

2. **Deploy from your project directory**:
```bash
vercel
```

3. **Follow the prompts**:
   - Set up and deploy? **Y**
   - Which scope? Choose your account
   - Link to existing project? **N** (for first deployment)
   - What's your project's name? **roseew-ai-chatbot**
   - In which directory is your code located? **./**

4. **Set Environment Variables** (during setup or later):
```bash
vercel env add OPENROUTER_API_KEY
vercel env add SECRET_KEY
```

5. **Deploy to production**:
```bash
vercel --prod
```

Your app will be live at a URL like: `https://roseew-ai-chatbot.vercel.app`

### Environment Variables Setup

After deployment, add your environment variables:

1. Go to your [Vercel Dashboard](https://vercel.com/dashboard)
2. Select your project
3. Go to **Settings** → **Environment Variables**
4. Add:
   - `OPENROUTER_API_KEY`: Your OpenRouter API key
   - `SECRET_KEY`: A secure random string

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
├── api/
│   └── index.py          # Vercel entry point
├── templates/
│   └── index.html        # Chat interface
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel deployment configuration
├── .env.example         # Environment variables template
├── .gitignore          # Git ignore rules
├── LICENSE             # MIT License
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

2. **Vercel Deployment Fails**:
   - Verify all files are committed to git
   - Check Vercel deployment logs in dashboard
   - Ensure environment variables are set on Vercel

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### MIT License Summary

- ✅ **Commercial use** - You can use this project commercially
- ✅ **Modification** - You can modify the code
- ✅ **Distribution** - You can distribute the code
- ✅ **Private use** - You can use it privately
- ⚠️ **Liability** - Authors are not liable for damages
- ⚠️ **Warranty** - No warranty is provided

Copyright (c) 2025 Roseew AI Chatbot

## 👨‍💻 Developer

**Varun Kumar Singh**

- 🌐 **Live Demo**: [https://roseew-ai-chatbot-boq0po5an.vercel.app](https://roseew-ai-chatbot.vercel.app/)
- 📧 **Email**: [varunkumarsingh818@gmail.com](mailto:varunkumarsingh818@gmail.com)
- 💼 **GitHub**: [@varunkm11](https://github.com/varunkm11)
- 🚀 **Project**: Roseew AI Chatbot - Advanced conversational AI with real-time capabilities

*Passionate full-stack developer creating innovative AI solutions and modern web applications.*

## Support

For issues and questions:
1. Check the troubleshooting section
2. Review deployment logs for any issues
3. Ensure all environment variables are configured correctly
4. Contact the developer: [varunkumarsingh818@gmail.com](mailto:varunkumarsingh818@gmail.com)

**Live Demo**: [https://roseew-ai-chatbot-boq0po5an.vercel.app](https://roseew-ai-chatbot-boq0po5an.vercel.app)

## Future Enhancements

Potential improvements:
- User authentication and chat history persistence
- File upload capabilities
- Voice message support
- Multiple AI model selection in UI
- Chat export functionality
- Custom theme options

---

<div align="center">

### 🤖 Roseew AI Chatbot

<div align="center">

**Developed with ❤️ by Varun Kumar Singh**

[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/varunkm11)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/varun-kumar-singh-267951269/)
[![Email](https://img.shields.io/badge/Email-D14836?style=for-the-badge&logo=gmail&logoColor=white)](mailto:varunkumarsingh818@gmail.com)

</div>

*Advanced AI Assistant with Real-Time Capabilities*

</div>
