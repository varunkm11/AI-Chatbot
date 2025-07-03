from flask import Flask, request, jsonify, render_template_string
from flask_cors import CORS
import requests
import json
import uuid
from datetime import datetime
from typing import Dict, List, Optional
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Flask App ---
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- Configuration ---
class Config:
    OPENROUTER_API_KEY = "your-openrouter-api-key"  # Set this in environment variables
    OPENROUTER_URL = "https://openrouter.ai/api/v1/chat/completions"
    
    MODELS = {
        "mistralai/mistral-7b-instruct": "Mistral 7B",
        "openai/gpt-3.5-turbo": "GPT-3.5 Turbo",
        "anthropic/claude-3-haiku": "Claude 3 Haiku",
        "google/gemma-7b-it": "Gemma 7B",
        "meta-llama/llama-3-8b-instruct": "Llama 3 8B"
    }

# --- In-memory storage (use Redis/Database in production) ---
conversations: Dict[str, List[Dict]] = {}

# --- Helper Functions ---
def get_ai_response(messages: List[Dict], model: str) -> Optional[Dict]:
    """Get response from AI model"""
    try:
        headers = {
            "Authorization": f"Bearer {Config.OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7,
            "stream": False
        }
        
        response = requests.post(Config.OPENROUTER_URL, headers=headers, json=data, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            logger.error(f"API Error {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        logger.error(f"Error getting AI response: {str(e)}")
        return None

def prepare_messages(user_input: str, conversation_id: str, system_prompt: str = None) -> List[Dict]:
    """Prepare messages for AI API"""
    messages = []
    
    if system_prompt:
        messages.append({"role": "system", "content": system_prompt})
    else:
        messages.append({
            "role": "system", 
            "content": "You are a helpful AI assistant. Be concise and accurate."
        })
    
    # Add conversation history
    if conversation_id in conversations:
        # Get last 10 exchanges to manage token count
        recent_messages = conversations[conversation_id][-20:]
        for msg in recent_messages:
            messages.append({"role": "user", "content": msg["user"]})
            messages.append({"role": "assistant", "content": msg["assistant"]})
    
    # Add current user input
    messages.append({"role": "user", "content": user_input})
    
    return messages

# --- API Routes ---
@app.route('/')
def index():
    return jsonify({
        "message": "Advanced AI Chatbot Flask API",
        "version": "1.0.0",
        "endpoints": {
            "chat": "/api/chat",
            "models": "/api/models",
            "conversations": "/api/conversations",
            "web_interface": "/web"
        }
    })

@app.route('/api/models', methods=['GET'])
def get_models():
    """Get available AI models"""
    return jsonify({"models": Config.MODELS})

@app.route('/api/chat', methods=['POST'])
def chat():
    """Send a chat message and get AI response"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Message is required"}), 400
        
        user_message = data['message']
        model = data.get('model', 'mistralai/mistral-7b-instruct')
        conversation_id = data.get('conversation_id', str(uuid.uuid4()))
        system_prompt = data.get('system_prompt')
        
        if not user_message.strip():
            return jsonify({"error": "Message cannot be empty"}), 400
        
        # Prepare messages
        messages = prepare_messages(user_message, conversation_id, system_prompt)
        
        # Get AI response
        response = get_ai_response(messages, model)
        
        if not response or 'choices' not in response:
            return jsonify({"error": "Failed to get AI response"}), 500
        
        ai_response = response['choices'][0]['message']['content']
        tokens_used = response.get('usage', {}).get('total_tokens', 0)
        
        # Store conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        conversations[conversation_id].append({
            "user": user_message,
            "assistant": ai_response,
            "timestamp": datetime.now().isoformat(),
            "model": model,
            "tokens": tokens_used
        })
        
        return jsonify({
            "response": ai_response,
            "conversation_id": conversation_id,
            "model": model,
            "timestamp": datetime.now().isoformat(),
            "tokens_used": tokens_used
        })
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        return jsonify({"error": str(e)}), 500

@app.route('/api/conversations', methods=['GET'])
def list_conversations():
    """List all conversation IDs"""
    return jsonify({
        "conversations": [
            {
                "id": conv_id,
                "message_count": len(messages),
                "last_updated": messages[-1]["timestamp"] if messages else None
            }
            for conv_id, messages in conversations.items()
        ]
    })

@app.route('/api/conversations/<conversation_id>', methods=['GET'])
def get_conversation(conversation_id):
    """Get conversation history"""
    if conversation_id not in conversations:
        return jsonify({"error": "Conversation not found"}), 404
    
    return jsonify({
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id],
        "total_messages": len(conversations[conversation_id])
    })

@app.route('/api/conversations/<conversation_id>', methods=['DELETE'])
def delete_conversation(conversation_id):
    """Delete conversation"""
    if conversation_id not in conversations:
        return jsonify({"error": "Conversation not found"}), 404
    
    del conversations[conversation_id]
    return jsonify({"message": "Conversation deleted successfully"})

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_conversations": len(conversations)
    })

# --- Web Interface ---
@app.route('/web')
def web_interface():
    """Simple web interface for the chatbot"""
    return render_template_string("""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Advanced AI Chatbot - Flask</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            body {
                font-family: Arial, sans-serif;
                max-width: 800px;
                margin: 0 auto;
                padding: 20px;
                background-color: #f5f5f5;
            }
            .chat-container {
                background: white;
                border-radius: 10px;
                padding: 20px;
                box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            }
            .chat-messages {
                height: 400px;
                overflow-y: auto;
                border: 1px solid #ddd;
                padding: 10px;
                margin-bottom: 20px;
                background-color: #fafafa;
            }
            .message {
                margin-bottom: 15px;
                padding: 10px;
                border-radius: 5px;
            }
            .user-message {
                background-color: #007bff;
                color: white;
                text-align: right;
            }
            .ai-message {
                background-color: #e9ecef;
                color: #333;
            }
            .input-container {
                display: flex;
                gap: 10px;
                margin-bottom: 10px;
            }
            input[type="text"] {
                flex: 1;
                padding: 10px;
                border: 1px solid #ddd;
                border-radius: 5px;
            }
            button {
                padding: 10px 20px;
                background-color: #007bff;
                color: white;
                border: none;
                border-radius: 5px;
                cursor: pointer;
            }
            button:hover {
                background-color: #0056b3;
            }
            .loading {
                font-style: italic;
                color: #666;
            }
            select {
                padding: 5px;
                margin-bottom: 10px;
                border-radius: 3px;
                border: 1px solid #ddd;
            }
            .model-selector {
                margin-bottom: 15px;
            }
            .stats {
                font-size: 12px;
                color: #666;
                margin-top: 10px;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h1>🤖 Advanced AI Chatbot (Flask)</h1>
            
            <div class="model-selector">
                <label for="model-select">AI Model:</label>
                <select id="model-select">
                    <option value="mistralai/mistral-7b-instruct">Mistral 7B</option>
                    <option value="openai/gpt-3.5-turbo">GPT-3.5 Turbo</option>
                    <option value="anthropic/claude-3-haiku">Claude 3 Haiku</option>
                    <option value="google/gemma-7b-it">Gemma 7B</option>
                    <option value="meta-llama/llama-3-8b-instruct">Llama 3 8B</option>
                </select>
            </div>
            
            <div class="chat-messages" id="chat-messages"></div>
            
            <div class="input-container">
                <input type="text" id="message-input" placeholder="Type your message here..." />
                <button onclick="sendMessage()">Send</button>
            </div>
            
            <div>
                <button onclick="clearChat()" style="background-color: #dc3545; margin-right: 10px;">Clear Chat</button>
                <button onclick="exportChat()" style="background-color: #28a745;">Export Chat</button>
            </div>
            
            <div class="stats" id="stats">
                Conversation ID: <span id="conversation-id"></span> | Messages: <span id="message-count">0</span>
            </div>
        </div>

        <script>
            let conversationId = generateUUID();
            let messageCount = 0;
            
            function generateUUID() {
                return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                    const r = Math.random() * 16 | 0;
                    const v = c == 'x' ? r : (r & 0x3 | 0x8);
                    return v.toString(16);
                });
            }
            
            function addMessage(message, sender) {
                const messagesDiv = document.getElementById('chat-messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.textContent = message;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                
                if (sender === 'user') {
                    messageCount++;
                    updateStats();
                }
            }
            
            function showLoading() {
                const messagesDiv = document.getElementById('chat-messages');
                const loadingDiv = document.createElement('div');
                loadingDiv.id = 'loading';
                loadingDiv.className = 'message ai-message loading';
                loadingDiv.textContent = 'AI is thinking...';
                messagesDiv.appendChild(loadingDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            function hideLoading() {
                const loadingDiv = document.getElementById('loading');
                if (loadingDiv) {
                    loadingDiv.remove();
                }
            }
            
            function updateStats() {
                document.getElementById('conversation-id').textContent = conversationId.substring(0, 8) + '...';
                document.getElementById('message-count').textContent = messageCount;
            }
            
            async function sendMessage() {
                const input = document.getElementById('message-input');
                const message = input.value.trim();
                const model = document.getElementById('model-select').value;
                
                if (!message) return;
                
                // Add user message
                addMessage(message, 'user');
                input.value = '';
                
                // Show loading
                showLoading();
                
                try {
                    const response = await fetch('/api/chat', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({
                            message: message,
                            model: model,
                            conversation_id: conversationId
                        })
                    });
                    
                    const data = await response.json();
                    
                    hideLoading();
                    
                    if (response.ok) {
                        addMessage(data.response, 'ai');
                        conversationId = data.conversation_id;
                    } else {
                        addMessage('Error: ' + data.error, 'ai');
                    }
                } catch (error) {
                    hideLoading();
                    addMessage('Error: ' + error.message, 'ai');
                }
            }
            
            function clearChat() {
                document.getElementById('chat-messages').innerHTML = '';
                conversationId = generateUUID();
                messageCount = 0;
                updateStats();
            }
            
            async function exportChat() {
                try {
                    const response = await fetch(`/api/conversations/${conversationId}`);
                    const data = await response.json();
                    
                    if (response.ok) {
                        const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
                        const url = URL.createObjectURL(blob);
                        const a = document.createElement('a');
                        a.href = url;
                        a.download = `chat_${conversationId.substring(0, 8)}.json`;
                        a.click();
                        URL.revokeObjectURL(url);
                    }
                } catch (error) {
                    alert('Error exporting chat: ' + error.message);
                }
            }
            
            // Initialize
            updateStats();
            
            // Send message on Enter key
            document.getElementById('message-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
