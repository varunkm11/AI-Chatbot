from fastapi import FastAPI, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
import requests
import json
import uuid
from datetime import datetime
from typing import List, Dict, Optional
import asyncio
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Pydantic Models ---
class ChatMessage(BaseModel):
    message: str
    model: str = "mistralai/mistral-7b-instruct"
    conversation_id: Optional[str] = None
    system_prompt: Optional[str] = None

class ChatResponse(BaseModel):
    response: str
    conversation_id: str
    model: str
    timestamp: str
    tokens_used: int

class ConversationHistory(BaseModel):
    conversation_id: str
    messages: List[Dict]
    created_at: str
    updated_at: str

# --- FastAPI App ---
app = FastAPI(
    title="Advanced AI Chatbot API",
    description="FastAPI backend for AI chatbot with WebSocket support",
    version="1.0.0"
)

# CORS middleware for web integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
active_connections: Dict[str, WebSocket] = {}

# --- Helper Functions ---
async def get_ai_response(messages: List[Dict], model: str) -> Optional[Dict]:
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

# --- API Endpoints ---
@app.get("/")
async def root():
    return {"message": "Advanced AI Chatbot API", "version": "1.0.0"}

@app.get("/models")
async def get_models():
    """Get available AI models"""
    return {"models": Config.MODELS}

@app.post("/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """Send a chat message and get AI response"""
    try:
        # Generate conversation ID if not provided
        conversation_id = message.conversation_id or str(uuid.uuid4())
        
        # Prepare messages
        messages = prepare_messages(message.message, conversation_id, message.system_prompt)
        
        # Get AI response
        response = await get_ai_response(messages, message.model)
        
        if not response or 'choices' not in response:
            raise HTTPException(status_code=500, detail="Failed to get AI response")
        
        ai_response = response['choices'][0]['message']['content']
        tokens_used = response.get('usage', {}).get('total_tokens', 0)
        
        # Store conversation
        if conversation_id not in conversations:
            conversations[conversation_id] = []
        
        conversations[conversation_id].append({
            "user": message.message,
            "assistant": ai_response,
            "timestamp": datetime.now().isoformat(),
            "model": message.model,
            "tokens": tokens_used
        })
        
        return ChatResponse(
            response=ai_response,
            conversation_id=conversation_id,
            model=message.model,
            timestamp=datetime.now().isoformat(),
            tokens_used=tokens_used
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/conversation/{conversation_id}")
async def get_conversation(conversation_id: str):
    """Get conversation history"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    return {
        "conversation_id": conversation_id,
        "messages": conversations[conversation_id],
        "total_messages": len(conversations[conversation_id])
    }

@app.delete("/conversation/{conversation_id}")
async def delete_conversation(conversation_id: str):
    """Delete conversation"""
    if conversation_id not in conversations:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    del conversations[conversation_id]
    return {"message": "Conversation deleted successfully"}

@app.get("/conversations")
async def list_conversations():
    """List all conversation IDs"""
    return {
        "conversations": [
            {
                "id": conv_id,
                "message_count": len(messages),
                "last_updated": messages[-1]["timestamp"] if messages else None
            }
            for conv_id, messages in conversations.items()
        ]
    }

# --- WebSocket for Real-time Chat ---
@app.websocket("/ws/{conversation_id}")
async def websocket_endpoint(websocket: WebSocket, conversation_id: str):
    await websocket.accept()
    active_connections[conversation_id] = websocket
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message
            user_message = message_data.get("message", "")
            model = message_data.get("model", "mistralai/mistral-7b-instruct")
            system_prompt = message_data.get("system_prompt")
            
            if user_message:
                # Send typing indicator
                await websocket.send_json({
                    "type": "typing",
                    "message": "AI is thinking..."
                })
                
                # Prepare messages
                messages = prepare_messages(user_message, conversation_id, system_prompt)
                
                # Get AI response
                response = await get_ai_response(messages, model)
                
                if response and 'choices' in response:
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
                    
                    # Send response to client
                    await websocket.send_json({
                        "type": "message",
                        "user_message": user_message,
                        "ai_response": ai_response,
                        "conversation_id": conversation_id,
                        "model": model,
                        "timestamp": datetime.now().isoformat(),
                        "tokens_used": tokens_used
                    })
                else:
                    await websocket.send_json({
                        "type": "error",
                        "message": "Failed to get AI response"
                    })
                    
    except WebSocketDisconnect:
        if conversation_id in active_connections:
            del active_connections[conversation_id]
        logger.info(f"WebSocket connection closed for conversation {conversation_id}")
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}")
        await websocket.close()

# --- Health Check ---
@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "active_conversations": len(conversations),
        "active_connections": len(active_connections)
    }

# --- Static Files (for web interface) ---
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- HTML Web Interface ---
@app.get("/web", response_class=HTMLResponse)
async def web_interface():
    """Simple web interface for the chatbot"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Advanced AI Chatbot</title>
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
            .typing {
                font-style: italic;
                color: #666;
            }
            select {
                padding: 5px;
                margin-bottom: 10px;
                border-radius: 3px;
                border: 1px solid #ddd;
            }
        </style>
    </head>
    <body>
        <div class="chat-container">
            <h1>🤖 Advanced AI Chatbot</h1>
            
            <div>
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
            
            <button onclick="clearChat()" style="margin-top: 10px; background-color: #dc3545;">Clear Chat</button>
        </div>

        <script>
            const conversationId = generateUUID();
            let ws = null;
            
            function generateUUID() {
                return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
                    const r = Math.random() * 16 | 0;
                    const v = c == 'x' ? r : (r & 0x3 | 0x8);
                    return v.toString(16);
                });
            }
            
            function connectWebSocket() {
                ws = new WebSocket(`ws://localhost:8000/ws/${conversationId}`);
                
                ws.onmessage = function(event) {
                    const data = JSON.parse(event.data);
                    if (data.type === 'message') {
                        addMessage(data.user_message, 'user');
                        addMessage(data.ai_response, 'ai');
                    } else if (data.type === 'typing') {
                        showTyping();
                    } else if (data.type === 'error') {
                        addMessage('Error: ' + data.message, 'ai');
                    }
                };
                
                ws.onopen = function() {
                    console.log('WebSocket connected');
                };
                
                ws.onclose = function() {
                    console.log('WebSocket disconnected');
                };
            }
            
            function addMessage(message, sender) {
                const messagesDiv = document.getElementById('chat-messages');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                messageDiv.textContent = message;
                messagesDiv.appendChild(messageDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
                
                // Remove typing indicator
                const typingDiv = document.querySelector('.typing');
                if (typingDiv) {
                    typingDiv.remove();
                }
            }
            
            function showTyping() {
                const messagesDiv = document.getElementById('chat-messages');
                const typingDiv = document.createElement('div');
                typingDiv.className = 'message ai-message typing';
                typingDiv.textContent = 'AI is thinking...';
                messagesDiv.appendChild(typingDiv);
                messagesDiv.scrollTop = messagesDiv.scrollHeight;
            }
            
            function sendMessage() {
                const input = document.getElementById('message-input');
                const message = input.value.trim();
                const model = document.getElementById('model-select').value;
                
                if (message && ws && ws.readyState === WebSocket.OPEN) {
                    ws.send(JSON.stringify({
                        message: message,
                        model: model
                    }));
                    input.value = '';
                }
            }
            
            function clearChat() {
                document.getElementById('chat-messages').innerHTML = '';
            }
            
            // Connect WebSocket on page load
            connectWebSocket();
            
            // Send message on Enter key
            document.getElementById('message-input').addEventListener('keypress', function(e) {
                if (e.key === 'Enter') {
                    sendMessage();
                }
            });
        </script>
    </body>
    </html>
    """

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
