import requests
import streamlit as st
import json
import time
from datetime import datetime
from typing import List, Dict, Optional
import uuid

# Import real-time data functionality
from realtime_data import RealTimeDataProvider, process_realtime_query, format_realtime_data

# --- Configuration ---
class ChatbotConfig:
    MODELS = {
        "mistralai/mistral-7b-instruct": "Mistral 7B (Fast)",
        "openai/gpt-3.5-turbo": "GPT-3.5 Turbo",
        "anthropic/claude-3-haiku": "Claude 3 Haiku",
        "google/gemma-7b-it": "Gemma 7B",
        "meta-llama/llama-3-8b-instruct": "Llama 3 8B"
    }
    
    MAX_HISTORY = 50
    DEFAULT_SYSTEM_PROMPT = """You are a helpful AI assistant. You are knowledgeable, friendly, and provide accurate information. 
    Always be concise but comprehensive in your responses."""

# --- Session State Initialization ---
def init_session_state():
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []
    if 'conversation_id' not in st.session_state:
        st.session_state.conversation_id = str(uuid.uuid4())
    if 'total_tokens' not in st.session_state:
        st.session_state.total_tokens = 0
    if 'system_prompt' not in st.session_state:
        st.session_state.system_prompt = ChatbotConfig.DEFAULT_SYSTEM_PROMPT
    if 'realtime_provider' not in st.session_state:
        st.session_state.realtime_provider = RealTimeDataProvider()

# --- API Functions ---
def get_ai_response(messages: List[Dict], model: str, api_key: str) -> Optional[Dict]:
    """Get response from AI model with error handling"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        
        data = {
            "model": model,
            "messages": messages,
            "max_tokens": 1000,
            "temperature": 0.7,
            "stream": False
        }
        
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions", 
            headers=headers, 
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            return response.json()
        else:
            st.error(f"API Error {response.status_code}: {response.text}")
            return None
            
    except requests.exceptions.RequestException as e:
        st.error(f"Network error: {str(e)}")
        return None
    except Exception as e:
        st.error(f"Unexpected error: {str(e)}")
        return None

def prepare_messages(user_input: str, chat_history: List[Dict], system_prompt: str) -> List[Dict]:
    """Prepare messages for AI API including system prompt and chat history"""
    messages = [{"role": "system", "content": system_prompt}]
    
    # Add recent chat history (last 10 exchanges to manage token count)
    recent_history = chat_history[-20:] if len(chat_history) > 20 else chat_history
    for chat in recent_history:
        messages.append({"role": "user", "content": chat["user"]})
        messages.append({"role": "assistant", "content": chat["assistant"]})
    
    # Add current user input
    messages.append({"role": "user", "content": user_input})
    
    return messages

# --- UI Components ---
def display_chat_history():
    """Display chat history with better formatting"""
    for i, chat in enumerate(st.session_state.chat_history):
        with st.container():
            # User message
            with st.chat_message("user"):
                st.write(chat["user"])
            
            # Assistant message
            with st.chat_message("assistant"):
                st.write(chat["assistant"])
            
            # Timestamp and metadata
            col1, col2, col3 = st.columns([2, 1, 1])
            with col1:
                if "timestamp" in chat:
                    st.caption(f"🕒 {chat['timestamp']}")
            with col2:
                if chat.get("realtime_data"):
                    st.caption("🔄 Real-time data")
            with col3:
                st.caption(f"🤖 {ChatbotConfig.MODELS.get(chat.get('model', ''), 'Unknown')}")
            
            st.divider()

def export_chat_history():
    """Export chat history as JSON"""
    if st.session_state.chat_history:
        export_data = {
            "conversation_id": st.session_state.conversation_id,
            "export_time": datetime.now().isoformat(),
            "total_messages": len(st.session_state.chat_history),
            "chat_history": st.session_state.chat_history
        }
        
        json_string = json.dumps(export_data, indent=2)
        st.download_button(
            label="📥 Download Chat History",
            data=json_string,
            file_name=f"chat_history_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
            mime="application/json"
        )

# --- Main Streamlit App ---
def main():
    # Page configuration
    st.set_page_config(
        page_title="Advanced AI Chatbot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialize session state
    init_session_state()
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
        color: white;
    }
    .chat-container {
        max-height: 600px;
        overflow-y: auto;
        padding: 1rem;
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        background-color: #f9f9f9;
    }
    .stats-card {
        background: #f0f2f6;
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown("""
    <div class="main-header">
        <h1>🤖 Advanced AI Chatbot</h1>
        <p>Intelligent conversations with multiple AI models</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar Configuration
    with st.sidebar:
        st.header("🛠️ Configuration")
        
        # Get API Key from secrets (hidden from UI)
        api_key = ""
        try:
            api_key = st.secrets["general"]["OPENROUTER_API_KEY"]
            st.success("✅ API Key loaded from secrets")
        except:
            st.error("⚠️ API Key not found in secrets.toml")
            st.stop()
        
        # Model Selection
        selected_model = st.selectbox(
            "🤖 Select AI Model",
            options=list(ChatbotConfig.MODELS.keys()),
            format_func=lambda x: ChatbotConfig.MODELS[x],
            index=0
        )
        
        # System Prompt
        st.subheader("📝 System Prompt")
        system_prompt = st.text_area(
            "Customize AI behavior",
            value=st.session_state.system_prompt,
            height=150,
            help="This prompt defines how the AI should behave"
        )
        
        if st.button("💾 Update System Prompt"):
            st.session_state.system_prompt = system_prompt
            st.success("System prompt updated!")
        
        st.divider()
        
        # Chat Statistics
        st.subheader("📊 Chat Statistics")
        st.markdown(f"""
        <div class="stats-card">
            <strong>💬 Total Messages:</strong> {len(st.session_state.chat_history)}<br>
            <strong>🆔 Conversation ID:</strong> {st.session_state.conversation_id[:8]}...<br>
            <strong>🤖 Current Model:</strong> {ChatbotConfig.MODELS[selected_model]}
        </div>
        """, unsafe_allow_html=True)
        
        st.divider()
        
        # Export and Clear
        if st.session_state.chat_history:
            export_chat_history()
            
            if st.button("🗑️ Clear Chat History", type="secondary"):
                st.session_state.chat_history = []
                st.session_state.conversation_id = str(uuid.uuid4())
                st.rerun()
    
    # Main Chat Interface
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.subheader("💬 Chat Interface")
        
        # Display chat history FIRST (before input)
        if st.session_state.chat_history:
            st.markdown("**📚 Conversation:**")
            with st.container():
                display_chat_history()
        else:
            st.info("👋 Start a conversation by typing a message below!")
        
        # Then show input area
        st.markdown("---")
        
        # Chat input
        user_input = st.text_input(
            "💭 Ask me anything...",
            placeholder="Type your question here...",
            key="user_input"
        )
        
        # Action buttons
        col_send, col_clear = st.columns([1, 1])
        
        with col_send:
            send_button = st.button("🚀 Send Message", type="primary", use_container_width=True)
        
        with col_clear:
            if st.button("🔄 New Conversation", use_container_width=True):
                st.session_state.chat_history = []
                st.session_state.conversation_id = str(uuid.uuid4())
                st.rerun()
    
    with col2:
        st.subheader("🎯 Quick Actions")
        
        # Predefined prompts
        st.info("💡 Try asking about:\n- Current time and date\n- Weather in London\n- Stock price of AAPL\n- Latest news\n- What is quantum computing\n- Exchange rate USD to EUR")
        
        # Real-time data toggle
        st.subheader("🔄 Real-time Data")
        realtime_enabled = st.checkbox("Enable real-time information", value=True, help="Get live data for time, weather, news, stocks, etc.")
        
        if realtime_enabled:
            st.success("✅ Real-time data enabled")
            st.caption("Ask about time, weather, news, stocks, Wikipedia, or exchange rates!")
        else:
            st.info("ℹ️ Real-time data disabled")
    
    # Process user input
    if send_button and user_input.strip():
        if not api_key:
            st.error("⚠️ API Key not found in secrets.toml")
            return
        
        # Show typing indicator
        with st.spinner("🤔 AI is thinking..."):
            # Check for real-time data request
            realtime_result = None
            if realtime_enabled:
                realtime_result = process_realtime_query(user_input, st.session_state.realtime_provider)
            
            # Prepare messages with real-time context
            messages = prepare_messages(user_input, st.session_state.chat_history, st.session_state.system_prompt)
            
            # Add real-time data to context if available
            if realtime_result:
                realtime_info = format_realtime_data(realtime_result)
                if realtime_info:
                    # Add real-time context to the system message
                    context_message = f"Current real-time information: {realtime_info}\n\nUser question: {user_input}"
                    messages[-1] = {"role": "user", "content": context_message}
            
            # Get AI response
            response = get_ai_response(messages, selected_model, api_key)
            
            if response and 'choices' in response:
                ai_response = response['choices'][0]['message']['content']
                
                # Add real-time data to response if available
                if realtime_result and format_realtime_data(realtime_result):
                    ai_response = format_realtime_data(realtime_result) + "\n\n" + ai_response
                
                # Add to chat history
                chat_entry = {
                    "user": user_input,
                    "assistant": ai_response,
                    "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "model": selected_model,
                    "tokens": response.get('usage', {}).get('total_tokens', 0),
                    "realtime_data": realtime_result is not None
                }
                
                st.session_state.chat_history.append(chat_entry)
                
                # Limit history size
                if len(st.session_state.chat_history) > ChatbotConfig.MAX_HISTORY:
                    st.session_state.chat_history = st.session_state.chat_history[-ChatbotConfig.MAX_HISTORY:]
                
                # Update token count
                st.session_state.total_tokens += chat_entry["tokens"]
                
                # Clear input and refresh
                st.rerun()
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style="text-align: center; color: #666; padding: 1rem;">
        <p>🤖 Advanced AI Chatbot | Built with Streamlit & OpenRouter API</p>
        <p>💡 Supports multiple AI models for enhanced conversations</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
