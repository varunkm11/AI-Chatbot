import os
import requests
import json
import time
import threading
import uuid
from flask import Flask, render_template, request, jsonify, session
from datetime import datetime, timedelta
import pytz
from dotenv import load_dotenv
from config import *
from models import db, ChatSession, ChatMessage, UserPreference

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY') or os.urandom(24).hex()

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///chatbot.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize database
db.init_app(app)

# Create tables
with app.app_context():
    db.create_all()

# OpenAI configuration
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')  # Load from environment variable only
OPENAI_URL = "https://api.openai.com/v1/chat/completions"

# Security check
if not OPENAI_API_KEY:
    print("⚠️  WARNING: OPENAI_API_KEY not found in environment variables!")
    print("📝 Please set your API key in the .env file")
elif OPENAI_API_KEY.startswith('your_'):
    print("⚠️  WARNING: Please replace the placeholder API key in .env file with your actual OpenAI API key")

class ChatBot:
    def __init__(self):
        # Remove in-memory storage as we're using database now
        pass
    
    def get_real_time_context(self):
        """Get real-time context information"""
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)
        return f"""Current date and time: {now.strftime('%Y-%m-%d %H:%M:%S')}
Today is {now.strftime('%A, %B %d, %Y')}
Current time: {now.strftime('%I:%M %p')} ({TIMEZONE})"""
    
    def get_ai_response(self, message, session_id, model=None):
        """Get response from OpenAI API"""
        if not OPENAI_API_KEY:
            return "Error: OpenAI API key not configured. Please set the OPENAI_API_KEY in config.py."
        
        # Get or create chat session
        chat_session = db.session.get(ChatSession, session_id)
        if not chat_session:
            chat_session = ChatSession(id=session_id, title=self._generate_title(message))
            db.session.add(chat_session)
            db.session.commit()
        
        # Get conversation history from database
        messages_query = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).limit(MAX_CONVERSATION_HISTORY)
        conversation_history = [{'role': msg.role, 'content': msg.content} for msg in messages_query]
        
        real_time_context = self.get_real_time_context()
        api_used = "OpenAI GPT"
        
        # Prepare messages
        messages = [
            {
                "role": "system",
                "content": f"""You are Roseew, a helpful AI assistant with access to real-time information.
                
{real_time_context}

You can provide current information and help with various tasks. Be conversational, helpful, and informative. Always introduce yourself as Roseew when asked about your name. If asked, tell the user you are using the {api_used} API for responses."""
            }
        ]
        
        # Add conversation history
        messages.extend(conversation_history)
        messages.append({"role": "user", "content": message})
        
        try:
            headers = {
                "Authorization": f"Bearer {OPENAI_API_KEY}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": model if model else AI_MODEL,
                "messages": messages,
                "temperature": TEMPERATURE,
                "max_tokens": MAX_TOKENS
            }
            
            response = requests.post(OPENAI_URL, headers=headers, json=data, timeout=30)
            response.raise_for_status()
            
            result = response.json()
            
            if 'choices' not in result or not result['choices']:
                return "Error: Invalid response from AI service"
            
            ai_response = result['choices'][0]['message']['content']
            
            # Save messages to database
            user_message = ChatMessage(
                session_id=session_id,
                role='user',
                content=message,
                model_used=model if model else AI_MODEL
            )
            
            assistant_message = ChatMessage(
                session_id=session_id,
                role='assistant',
                content=ai_response,
                model_used=model if model else AI_MODEL
            )
            
            db.session.add(user_message)
            db.session.add(assistant_message)
            
            # Update session timestamp
            chat_session.updated_at = datetime.now()
            
            db.session.commit()
            
            return ai_response
            
        except requests.exceptions.Timeout:
            return "Error: Request timed out. Please try again."
        except requests.exceptions.RequestException as e:
            error_msg = str(e)
            if "402" in error_msg or "Payment Required" in error_msg:
                return "⚠️ **Insufficient Credits**: Your OpenAI account needs credits. Please:\n1. Visit https://platform.openai.com/account/billing\n2. Add credits to your account\n\n💡 **Tip**: GPT-3.5-turbo is the most cost-effective option!"
            elif "401" in error_msg or "Unauthorized" in error_msg:
                return "🔑 **API Key Error**: Please check your OpenAI API key in config.py."
            elif "429" in error_msg or "rate limit" in error_msg.lower():
                return "⏰ **Rate Limited**: Too many requests. Please wait a moment and try again."
            return f"🌐 **Connection Error**: {error_msg}"
        except KeyError as e:
            return f"📝 **Response Error**: Invalid AI service response. Please try again or switch models."
        except Exception as e:
            return f"❌ **Unexpected Error**: {str(e)}"
    
    def _generate_title(self, first_message):
        """Generate a title for the chat session based on the first message"""
        # Simple title generation - take first 50 characters
        title = first_message[:50].strip()
        if len(first_message) > 50:
            title += "..."
        return title or "New Chat"

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
        if not data:
            return jsonify({'error': 'No JSON data provided'}), 400
            
        message = data.get('message', '').strip()
        model = data.get('model', AI_MODEL)  # Get model from request
        
        if not message:
            return jsonify({'error': 'Empty message'}), 400
        
        # Validate message length
        if len(message) > MAX_MESSAGE_LENGTH:
            return jsonify({'error': f'Message too long (max {MAX_MESSAGE_LENGTH} characters)'}), 400
        
        conversation_id = session.get('conversation_id', str(uuid.uuid4()))
        session['conversation_id'] = conversation_id
        
        # Get AI response with selected model
        response = chatbot.get_ai_response(message, conversation_id, model)
        
        tz = pytz.timezone(TIMEZONE)
        now = datetime.now(tz)
        return jsonify({
            'response': response,
            'timestamp': now.strftime('%H:%M'),
            'model_used': model
        })
        
    except Exception as e:
        return jsonify({'error': f'Internal server error: {str(e)}'}), 500

@app.route('/new-chat', methods=['POST'])
def new_chat():
    """Start a new conversation"""
    session['conversation_id'] = str(uuid.uuid4())
    return jsonify({'success': True})

# Endpoint to get chat history
@app.route('/history', methods=['GET'])
def get_history():
    conversation_id = session.get('conversation_id')
    if not conversation_id:
        return jsonify({'history': [], 'sessions': []})
    
    # Get current session messages
    messages = ChatMessage.query.filter_by(session_id=conversation_id).order_by(ChatMessage.timestamp).all()
    history = [{'role': msg.role, 'content': msg.content} for msg in messages]
    
    # Get all sessions for sidebar
    sessions = ChatSession.query.order_by(ChatSession.updated_at.desc()).limit(10).all()
    sessions_data = [session.to_dict() for session in sessions]
    
    return jsonify({
        'history': history,
        'sessions': sessions_data
    })

# Endpoint to delete chat history
@app.route('/delete-history', methods=['POST'])
def delete_history():
    conversation_id = session.get('conversation_id')
    if conversation_id:
        # Delete all messages for this session
        ChatMessage.query.filter_by(session_id=conversation_id).delete()
        # Delete the session
        ChatSession.query.filter_by(id=conversation_id).delete()
        db.session.commit()
    return jsonify({'success': True})

# Endpoint to delete a specific chat session
@app.route('/delete-session/<session_id>', methods=['DELETE'])
def delete_session(session_id):
    """Delete a specific chat session and all its messages"""
    try:
        # Check if session exists
        chat_session = db.session.get(ChatSession, session_id)
        if not chat_session:
            return jsonify({'error': 'Session not found'}), 404
        
        # Delete all messages for this session
        ChatMessage.query.filter_by(session_id=session_id).delete()
        
        # Delete the session
        db.session.delete(chat_session)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Chat session deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete session: {str(e)}'}), 500

# Endpoint to delete all chat history
@app.route('/delete-all-history', methods=['POST'])
def delete_all_history():
    """Delete all chat sessions and messages"""
    try:
        # Delete all messages
        ChatMessage.query.delete()
        # Delete all sessions
        ChatSession.query.delete()
        db.session.commit()
        
        # Start a new session
        session['conversation_id'] = str(uuid.uuid4())
        
        return jsonify({'success': True, 'message': 'All chat history deleted successfully'})
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Failed to delete all history: {str(e)}'}), 500

@app.route('/load-session/<session_id>', methods=['GET'])
def load_session(session_id):
    """Load a specific chat session"""
    chat_session = db.session.get(ChatSession, session_id)
    if not chat_session:
        return jsonify({'error': 'Session not found'}), 404
    
    # Update current session
    session['conversation_id'] = session_id
    
    # Get messages for this session
    messages = ChatMessage.query.filter_by(session_id=session_id).order_by(ChatMessage.timestamp).all()
    messages_data = [msg.to_dict() for msg in messages]
    
    return jsonify({
        'session': chat_session.to_dict(),
        'messages': messages_data
    })

@app.route('/health')
def health():
    """Health check endpoint for Heroku"""
    tz = pytz.timezone(TIMEZONE)
    now = datetime.now(tz)
    return jsonify({'status': 'healthy', 'timestamp': now.isoformat()})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)
