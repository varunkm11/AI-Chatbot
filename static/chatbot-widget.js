/**
 * Advanced AI Chatbot Widget
 * Can be embedded in any website
 */

class ChatbotWidget {
    constructor(options = {}) {
        this.options = {
            apiUrl: options.apiUrl || 'http://localhost:8000',
            position: options.position || 'bottom-right',
            theme: options.theme || 'light',
            model: options.model || 'mistralai/mistral-7b-instruct',
            title: options.title || 'AI Assistant',
            placeholder: options.placeholder || 'Type your message...',
            apiKey: options.apiKey || '',
            ...options
        };
        
        this.isOpen = false;
        this.conversationId = this.generateUUID();
        this.messages = [];
        
        this.init();
    }
    
    generateUUID() {
        return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, function(c) {
            const r = Math.random() * 16 | 0;
            const v = c == 'x' ? r : (r & 0x3 | 0x8);
            return v.toString(16);
        });
    }
    
    init() {
        this.createStyles();
        this.createWidget();
        this.bindEvents();
    }
    
    createStyles() {
        const styles = `
            .chatbot-widget {
                position: fixed;
                z-index: 9999;
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            }
            
            .chatbot-widget.bottom-right {
                bottom: 20px;
                right: 20px;
            }
            
            .chatbot-widget.bottom-left {
                bottom: 20px;
                left: 20px;
            }
            
            .chatbot-widget.top-right {
                top: 20px;
                right: 20px;
            }
            
            .chatbot-widget.top-left {
                top: 20px;
                left: 20px;
            }
            
            .chatbot-toggle {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                border: none;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 24px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                transition: all 0.3s ease;
            }
            
            .chatbot-toggle:hover {
                transform: scale(1.1);
                box-shadow: 0 6px 16px rgba(0,0,0,0.3);
            }
            
            .chatbot-container {
                position: absolute;
                bottom: 70px;
                right: 0;
                width: 350px;
                height: 500px;
                background: white;
                border-radius: 12px;
                box-shadow: 0 8px 32px rgba(0,0,0,0.2);
                display: none;
                flex-direction: column;
                overflow: hidden;
            }
            
            .chatbot-widget.top-right .chatbot-container,
            .chatbot-widget.top-left .chatbot-container {
                bottom: auto;
                top: 70px;
            }
            
            .chatbot-widget.bottom-left .chatbot-container,
            .chatbot-widget.top-left .chatbot-container {
                right: auto;
                left: 0;
            }
            
            .chatbot-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 16px;
                display: flex;
                align-items: center;
                justify-content: space-between;
            }
            
            .chatbot-title {
                font-weight: 600;
                font-size: 16px;
            }
            
            .chatbot-close {
                background: none;
                border: none;
                color: white;
                font-size: 18px;
                cursor: pointer;
                padding: 4px;
            }
            
            .chatbot-messages {
                flex: 1;
                overflow-y: auto;
                padding: 16px;
                background-color: #f8f9fa;
            }
            
            .chatbot-message {
                margin-bottom: 12px;
                animation: fadeIn 0.3s ease;
            }
            
            .chatbot-message.user {
                text-align: right;
            }
            
            .chatbot-message.user .message-content {
                background: #007bff;
                color: white;
                border-radius: 18px 18px 4px 18px;
                padding: 12px 16px;
                display: inline-block;
                max-width: 80%;
                word-wrap: break-word;
            }
            
            .chatbot-message.ai .message-content {
                background: white;
                color: #333;
                border-radius: 18px 18px 18px 4px;
                padding: 12px 16px;
                display: inline-block;
                max-width: 80%;
                word-wrap: break-word;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
            }
            
            .chatbot-input-area {
                padding: 16px;
                background: white;
                border-top: 1px solid #e9ecef;
                display: flex;
                gap: 8px;
            }
            
            .chatbot-input {
                flex: 1;
                border: 1px solid #ddd;
                border-radius: 20px;
                padding: 8px 16px;
                outline: none;
                font-size: 14px;
            }
            
            .chatbot-input:focus {
                border-color: #007bff;
            }
            
            .chatbot-send {
                background: #007bff;
                color: white;
                border: none;
                border-radius: 50%;
                width: 36px;
                height: 36px;
                cursor: pointer;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 16px;
            }
            
            .chatbot-send:hover {
                background: #0056b3;
            }
            
            .chatbot-send:disabled {
                background: #ccc;
                cursor: not-allowed;
            }
            
            .typing-indicator {
                display: flex;
                align-items: center;
                gap: 4px;
                padding: 12px 16px;
                background: white;
                border-radius: 18px 18px 18px 4px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                max-width: 80%;
            }
            
            .typing-dot {
                width: 6px;
                height: 6px;
                border-radius: 50%;
                background: #666;
                animation: typing 1.4s infinite;
            }
            
            .typing-dot:nth-child(2) {
                animation-delay: 0.2s;
            }
            
            .typing-dot:nth-child(3) {
                animation-delay: 0.4s;
            }
            
            @keyframes typing {
                0%, 60%, 100% {
                    transform: scale(1);
                    opacity: 0.5;
                }
                30% {
                    transform: scale(1.2);
                    opacity: 1;
                }
            }
            
            @keyframes fadeIn {
                from {
                    opacity: 0;
                    transform: translateY(10px);
                }
                to {
                    opacity: 1;
                    transform: translateY(0);
                }
            }
            
            .chatbot-widget.dark .chatbot-container {
                background: #2c3e50;
            }
            
            .chatbot-widget.dark .chatbot-messages {
                background: #34495e;
            }
            
            .chatbot-widget.dark .chatbot-message.ai .message-content {
                background: #3c4c5c;
                color: #ecf0f1;
            }
            
            .chatbot-widget.dark .chatbot-input-area {
                background: #2c3e50;
                border-color: #5a6c7d;
            }
            
            .chatbot-widget.dark .chatbot-input {
                background: #34495e;
                border-color: #5a6c7d;
                color: #ecf0f1;
            }
            
            @media (max-width: 480px) {
                .chatbot-container {
                    width: 300px;
                    height: 400px;
                }
            }
        `;
        
        const styleSheet = document.createElement('style');
        styleSheet.textContent = styles;
        document.head.appendChild(styleSheet);
    }
    
    createWidget() {
        const widget = document.createElement('div');
        widget.className = `chatbot-widget ${this.options.position} ${this.options.theme}`;
        
        widget.innerHTML = `
            <button class="chatbot-toggle" aria-label="Open chat">
                💬
            </button>
            
            <div class="chatbot-container">
                <div class="chatbot-header">
                    <div class="chatbot-title">${this.options.title}</div>
                    <button class="chatbot-close" aria-label="Close chat">✕</button>
                </div>
                
                <div class="chatbot-messages" id="chatbot-messages"></div>
                
                <div class="chatbot-input-area">
                    <input type="text" class="chatbot-input" placeholder="${this.options.placeholder}" id="chatbot-input">
                    <button class="chatbot-send" aria-label="Send message">➤</button>
                </div>
            </div>
        `;
        
        document.body.appendChild(widget);
        this.widget = widget;
        
        // Add welcome message
        this.addMessage('Hello! I\'m your AI assistant. How can I help you today?', 'ai');
    }
    
    bindEvents() {
        const toggle = this.widget.querySelector('.chatbot-toggle');
        const close = this.widget.querySelector('.chatbot-close');
        const input = this.widget.querySelector('.chatbot-input');
        const send = this.widget.querySelector('.chatbot-send');
        
        toggle.addEventListener('click', () => this.toggle());
        close.addEventListener('click', () => this.close());
        send.addEventListener('click', () => this.sendMessage());
        
        input.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') {
                this.sendMessage();
            }
        });
    }
    
    toggle() {
        this.isOpen = !this.isOpen;
        const container = this.widget.querySelector('.chatbot-container');
        container.style.display = this.isOpen ? 'flex' : 'none';
        
        if (this.isOpen) {
            this.widget.querySelector('.chatbot-input').focus();
        }
    }
    
    close() {
        this.isOpen = false;
        const container = this.widget.querySelector('.chatbot-container');
        container.style.display = 'none';
    }
    
    addMessage(content, sender) {
        const messagesContainer = this.widget.querySelector('.chatbot-messages');
        const messageDiv = document.createElement('div');
        messageDiv.className = `chatbot-message ${sender}`;
        
        const messageContent = document.createElement('div');
        messageContent.className = 'message-content';
        messageContent.textContent = content;
        
        messageDiv.appendChild(messageContent);
        messagesContainer.appendChild(messageDiv);
        
        // Scroll to bottom
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
        
        // Store message
        this.messages.push({ content, sender, timestamp: new Date().toISOString() });
    }
    
    showTyping() {
        const messagesContainer = this.widget.querySelector('.chatbot-messages');
        const typingDiv = document.createElement('div');
        typingDiv.className = 'chatbot-message ai';
        typingDiv.id = 'typing-indicator';
        
        const typingContent = document.createElement('div');
        typingContent.className = 'typing-indicator';
        typingContent.innerHTML = `
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
            <div class="typing-dot"></div>
        `;
        
        typingDiv.appendChild(typingContent);
        messagesContainer.appendChild(typingDiv);
        messagesContainer.scrollTop = messagesContainer.scrollHeight;
    }
    
    hideTyping() {
        const typingIndicator = this.widget.querySelector('#typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }
    }
    
    async sendMessage() {
        const input = this.widget.querySelector('.chatbot-input');
        const send = this.widget.querySelector('.chatbot-send');
        const message = input.value.trim();
        
        if (!message) return;
        
        // Disable input
        input.disabled = true;
        send.disabled = true;
        
        // Add user message
        this.addMessage(message, 'user');
        input.value = '';
        
        // Show typing indicator
        this.showTyping();
        
        try {
            const response = await fetch(`${this.options.apiUrl}/api/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    message: message,
                    model: this.options.model,
                    conversation_id: this.conversationId
                })
            });
            
            const data = await response.json();
            
            this.hideTyping();
            
            if (response.ok) {
                this.addMessage(data.response, 'ai');
                this.conversationId = data.conversation_id;
            } else {
                this.addMessage('Sorry, I encountered an error. Please try again.', 'ai');
            }
        } catch (error) {
            this.hideTyping();
            this.addMessage('Sorry, I\'m having trouble connecting. Please try again.', 'ai');
        }
        
        // Re-enable input
        input.disabled = false;
        send.disabled = false;
        input.focus();
    }
    
    // Public API methods
    open() {
        if (!this.isOpen) {
            this.toggle();
        }
    }
    
    destroy() {
        if (this.widget) {
            this.widget.remove();
        }
    }
    
    setModel(model) {
        this.options.model = model;
    }
    
    clearConversation() {
        this.conversationId = this.generateUUID();
        this.messages = [];
        const messagesContainer = this.widget.querySelector('.chatbot-messages');
        messagesContainer.innerHTML = '';
        this.addMessage('Hello! I\'m your AI assistant. How can I help you today?', 'ai');
    }
}

// Auto-initialize if data attributes are present
document.addEventListener('DOMContentLoaded', () => {
    const chatbotElement = document.querySelector('[data-chatbot]');
    if (chatbotElement) {
        const options = {
            apiUrl: chatbotElement.dataset.apiUrl,
            position: chatbotElement.dataset.position,
            theme: chatbotElement.dataset.theme,
            model: chatbotElement.dataset.model,
            title: chatbotElement.dataset.title,
            placeholder: chatbotElement.dataset.placeholder
        };
        
        // Remove undefined values
        Object.keys(options).forEach(key => {
            if (options[key] === undefined) {
                delete options[key];
            }
        });
        
        new ChatbotWidget(options);
    }
});

// Make available globally
window.ChatbotWidget = ChatbotWidget;
