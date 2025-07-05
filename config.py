# Configuration settings for the AI Chatbot

# AI Model Configuration
AI_MODEL = "anthropic/claude-3.5-sonnet"  # Default AI model
MAX_TOKENS = 1000  # Maximum tokens per response
TEMPERATURE = 0.7  # AI creativity/randomness (0.0 to 1.0)

# Chat Configuration
MAX_CONVERSATION_HISTORY = 20  # Number of messages to keep in memory
CONVERSATION_TIMEOUT = 3600  # Session timeout in seconds (1 hour)

# Real-time Features
INCLUDE_TIMESTAMP = True  # Include current time in AI context
INCLUDE_DATE = True  # Include current date in AI context
TIMEZONE = "UTC"  # Default timezone for timestamps

# UI Configuration
CHAT_TITLE = "AI Assistant"  # Title shown in header
WELCOME_MESSAGE = """Hello! I'm your AI assistant with real-time capabilities. 
I can help you with questions, provide current information, and assist with various tasks. 
How can I help you today?"""

# Available AI Models (you can switch between these)
AVAILABLE_MODELS = [
    "anthropic/claude-3.5-sonnet",
    "anthropic/claude-3-opus",
    "openai/gpt-4-turbo",
    "openai/gpt-3.5-turbo",
    "google/gemini-pro",
    "meta-llama/llama-2-70b-chat",
    "mistralai/mixtral-8x7b-instruct"
]

# Rate Limiting (optional - for future implementation)
RATE_LIMIT_REQUESTS = 100  # Requests per hour per user
RATE_LIMIT_WINDOW = 3600  # Time window in seconds
