import os
import requests
import json
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime
import uuid
from dotenv import load_dotenv
from config import *

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'your-secret-key-here')

# OpenRouter configuration
OPENROUTER_API_KEY = os.environ.get('OPENROUTER_API_KEY')
OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"

class ChatBot:
    def __init__(self):
        self.conversations = {}
    
    def get_real_time_context(self):
        """Get real-time context information"""
        now = datetime.now()
        return f"""Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}
Today is {now.strftime('%A, %B %d, %Y')}
Current time: {now.strftime('%I:%M %p')}"""
    
    def get_ai_response(self, message, conversation_id):
        """Get response from OpenRouter AI"""
        if not OPENROUTER_API_KEY:
            return "Error: OpenRouter API key not configured. Please set the OPENROUTER_API_KEY environment variable."
        
        # Get or create conversation history
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        # Add real-time context to system message
        real_time_context = self.get_real_time_context()
        
        # Prepare messages with context
        messages = [
            {
                "role": "system",
                "content": f"""You are a helpful AI assistant with access to real-time information.
                
{real_time_context}

You can provide current information and help with various tasks. Be conversational, helpful, and informative."""
            }
        ]
        
        # Add conversation history
        messages.extend(self.conversations[conversation_id])
        
        # Add current message
        messages.append({"role": "user", "content": message})
        
        try:
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost:5000",
                "X-Title": "AI Chatbot"
            }
            
            data = {
                "model": AI_MODEL,
                "messages": messages,
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS
            }
            
            response = requests.post(OPENROUTER_URL, headers=headers, json=data)
            response.raise_for_status()
            
            result = response.json()
            ai_response = result['choices'][0]['message']['content']
            
            # Update conversation history
            self.conversations[conversation_id].append({"role": "user", "content": message})
            self.conversations[conversation_id].append({"role": "assistant", "content": ai_response})
            
            # Keep only last exchanges to manage memory
            if len(self.conversations[conversation_id]) > MAX_CONVERSATION_HISTORY:
                self.conversations[conversation_id] = self.conversations[conversation_id][-MAX_CONVERSATION_HISTORY:]
            
            return ai_response
            
        except requests.exceptions.RequestException as e:
            return f"Error connecting to AI service: {str(e)}"
        except KeyError as e:
            return f"Error parsing AI response: {str(e)}"
        except Exception as e:
            return f"Unexpected error: {str(e)}"

# Initialize chatbot
chatbot = ChatBot()

@app.route('/')
def index():
    # Create new conversation ID if not exists
    if 'conversation_id' not in session:
        session['conversation_id'] = str(uuid.uuid4())
    return render_template('index.html')

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.json
        message = data.get('message', '').strip()
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        conversation_id = session.get('conversation_id', str(uuid.uuid4()))
        session['conversation_id'] = conversation_id
        
        # Get AI response
        response = chatbot.get_ai_response(message, conversation_id)
        
        return jsonify({
            'response': response,
            'timestamp': datetime.now().strftime('%H:%M')
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/new-chat', methods=['POST'])
def new_chat():
    """Start a new conversation"""
    session['conversation_id'] = str(uuid.uuid4())
    return jsonify({'success': True})

@app.route('/health')
def health():
    """Health check endpoint for Heroku"""
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)
