from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timezone
import json

db = SQLAlchemy()

class ChatSession(db.Model):
    """Model for chat sessions"""
    __tablename__ = 'chat_sessions'
    
    id = db.Column(db.String(36), primary_key=True)  # UUID
    title = db.Column(db.String(100), nullable=False, default='New Chat')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    # Relationship to messages
    messages = db.relationship('ChatMessage', backref='session', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'message_count': len(self.messages)
        }

class ChatMessage(db.Model):
    """Model for individual chat messages"""
    __tablename__ = 'chat_messages'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(36), db.ForeignKey('chat_sessions.id'), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'user' or 'assistant'
    content = db.Column(db.Text, nullable=False)
    model_used = db.Column(db.String(100), nullable=True)  # AI model used for this message
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    
    def to_dict(self):
        return {
            'id': self.id,
            'role': self.role,
            'content': self.content,
            'model_used': self.model_used,
            'timestamp': self.timestamp.isoformat()
        }

class UserPreference(db.Model):
    """Model for user preferences"""
    __tablename__ = 'user_preferences'
    
    id = db.Column(db.Integer, primary_key=True)
    user_session = db.Column(db.String(36), nullable=False, unique=True)
    preferred_model = db.Column(db.String(100), default='anthropic/claude-3.5-sonnet')
    theme = db.Column(db.String(20), default='dark')
    settings = db.Column(db.Text)  # JSON string for additional settings
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    
    def get_settings(self):
        if self.settings:
            return json.loads(self.settings)
        return {}
    
    def set_settings(self, settings_dict):
        self.settings = json.dumps(settings_dict)
    
    def to_dict(self):
        return {
            'preferred_model': self.preferred_model,
            'theme': self.theme,
            'settings': self.get_settings()
        }
