#!/usr/bin/env python3
"""
Database setup script for the AI Chatbot
Run this script to initialize the database
"""

import os
from app import app, db
from models import ChatSession, ChatMessage, UserPreference

def init_database():
    """Initialize the database with all tables"""
    with app.app_context():
        try:
            # Create all tables
            db.create_all()
            print("✅ Database tables created successfully!")
            
            # Verify tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print(f"📋 Created tables: {', '.join(tables)}")
            
            return True
        except Exception as e:
            print(f"❌ Database initialization failed: {e}")
            return False

def reset_database():
    """Reset the database (WARNING: This will delete all data!)"""
    with app.app_context():
        print("⚠️  WARNING: This will delete all existing data!")
        confirm = input("Are you sure you want to reset the database? (yes/no): ")
        
        if confirm.lower() == 'yes':
            db.drop_all()
            db.create_all()
            print("✅ Database reset successfully!")
        else:
            print("❌ Database reset cancelled.")

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "--reset":
        reset_database()
    else:
        init_database()
