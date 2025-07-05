#!/usr/bin/env python3
"""
Test script for AI Chatbot
Run this to verify your setup before deployment
"""

import os
import sys
from datetime import datetime

def check_files():
    """Check if all required files exist"""
    required_files = [
        'app.py',
        'requirements.txt',
        'Procfile',
        'runtime.txt',
        'templates/index.html',
        'config.py'
    ]
    
    print("🔍 Checking required files...")
    missing_files = []
    
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            missing_files.append(file)
    
    return len(missing_files) == 0

def check_environment():
    """Check environment variables"""
    print("\n🔍 Checking environment variables...")
    
    required_vars = ['OPENROUTER_API_KEY', 'SECRET_KEY']
    missing_vars = []
    
    for var in required_vars:
        if os.environ.get(var):
            print(f"✅ {var} is set")
        else:
            print(f"❌ {var} is missing")
            missing_vars.append(var)
    
    return len(missing_vars) == 0

def check_dependencies():
    """Check if required packages can be imported"""
    print("\n🔍 Checking dependencies...")
    
    required_packages = [
        ('flask', 'Flask'),
        ('requests', 'requests'),
    ]
    
    missing_packages = []
    
    for package, import_name in required_packages:
        try:
            __import__(import_name.lower())
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package}")
            missing_packages.append(package)
    
    return len(missing_packages) == 0

def test_app_import():
    """Test if the app can be imported"""
    print("\n🔍 Testing app import...")
    
    try:
        from app import app
        print("✅ App imports successfully")
        return True
    except Exception as e:
        print(f"❌ App import failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 AI Chatbot Setup Test")
    print("=" * 40)
    
    tests = [
        check_files,
        check_dependencies,
        check_environment,
        test_app_import
    ]
    
    results = []
    for test in tests:
        results.append(test())
    
    print("\n" + "=" * 40)
    if all(results):
        print("🎉 All tests passed! Your chatbot is ready to deploy.")
        print("\nNext steps:")
        print("1. Set your environment variables in .env file")
        print("2. Test locally: python app.py")
        print("3. Deploy to Heroku: git push heroku main")
    else:
        print("❌ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()
