# Configuration settings for the AI Chatbot
import os

# API Configuration - Multiple Options
API_PROVIDER = os.environ.get('API_PROVIDER', 'openrouter')  # openai, openrouter, groq

# OpenAI API Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')  # Load from environment variable
OPENAI_BASE_URL = "https://api.openai.com/v1"

# OpenRouter API Configuration (Better rate limits, multiple models)
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
OPENROUTER_BASE_URL = "https://openrouter.ai/api/v1"

# Groq API Configuration (Very fast, generous free tier)
GROQ_API_KEY = os.environ.get('GROQ_API_KEY')
GROQ_BASE_URL = "https://api.groq.com/openai/v1"

# AI Model Configuration
AI_MODEL = "meta-llama/llama-3.1-8b-instruct:free"  # Default free model
MAX_TOKENS = 1000  # Maximum tokens per response
TEMPERATURE = 0.7  # AI creativity/randomness (0.0 to 1.0)

# Chat Configuration
MAX_CONVERSATION_HISTORY = 20  # Number of messages to keep in memory
CONVERSATION_TIMEOUT = 3600  # Session timeout in seconds (1 hour)
MAX_MESSAGE_LENGTH = 2000  # Maximum characters per message

# Real-time Features
INCLUDE_TIMESTAMP = True  # Include current time in AI context
INCLUDE_DATE = True  # Include current date in AI context
TIMEZONE = "Asia/Kolkata"  # Default timezone for timestamps

# UI Configuration
CHAT_TITLE = "Roseew"  # Title shown in header
WELCOME_MESSAGE = """Hello! I'm Roseew, your AI assistant with real-time capabilities. 
I can help you with questions, provide current information, and assist with various tasks. 
How can I help you today?"""

# Available AI Models by Provider
AVAILABLE_MODELS = {
    'openai': [
        "gpt-3.5-turbo",
        "gpt-4",
        "gpt-4-turbo", 
        "gpt-4o",
        "gpt-4o-mini"
    ],
    'openrouter': [
        # Free Models
        "meta-llama/llama-3.1-8b-instruct:free",
        "mistralai/mistral-7b-instruct:free",
        "microsoft/phi-3-mini-128k-instruct:free",
        "google/gemma-7b-it:free",
        # Paid Models (cheaper than OpenAI direct)
        "anthropic/claude-3.5-sonnet",
        "openai/gpt-4-turbo",
        "openai/gpt-3.5-turbo",
        "google/gemini-pro"
    ],
    'groq': [
        "mixtral-8x7b-32768",
        "llama2-70b-4096",
        "gemma-7b-it"
    ]
}

# Rate Limiting Configuration
RATE_LIMIT_REQUESTS = 20  # Requests per hour per user (reduced from 100)
RATE_LIMIT_WINDOW = 3600  # Time window in seconds
MIN_REQUEST_INTERVAL = 2  # Minimum seconds between requests
MAX_RETRIES = 3  # Maximum retry attempts for rate limited requests
BASE_RETRY_DELAY = 1  # Base delay for exponential backoff (seconds)
