# Configuration settings for the AI Chatbot
import os

# OpenAI API Configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')  # Load from environment variable
OPENAI_BASE_URL = "https://api.openai.com/v1"

# AI Model Configuration
AI_MODEL = "gpt-3.5-turbo"  # Default OpenAI model
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

# Available AI Models (OpenAI models)
AVAILABLE_MODELS = [
    "gpt-3.5-turbo",
    "gpt-4",
    "gpt-4-turbo", 
    "gpt-4o",
    "gpt-4o-mini"
]

# Rate Limiting Configuration
RATE_LIMIT_REQUESTS = 20  # Requests per hour per user (reduced from 100)
RATE_LIMIT_WINDOW = 3600  # Time window in seconds
MIN_REQUEST_INTERVAL = 2  # Minimum seconds between requests
MAX_RETRIES = 3  # Maximum retry attempts for rate limited requests
BASE_RETRY_DELAY = 1  # Base delay for exponential backoff (seconds)
