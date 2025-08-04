# 🔐 Security Guide

## API Key Security

### ✅ **Current Security Status**
Your API key is now properly secured:

1. **Environment Variables**: API key is stored in `.env` file only
2. **Git Ignored**: `.env` file is excluded from version control
3. **No Hardcoding**: Removed hardcoded API key from `config.py`
4. **Runtime Checks**: Added validation to ensure proper setup

### 🚨 **Security Best Practices**

#### 1. **Never Commit API Keys**
- ❌ Don't put API keys in source code
- ❌ Don't commit `.env` files to git
- ✅ Use `.env.example` for templates
- ✅ Add `.env` to `.gitignore`

#### 2. **Environment Variable Usage**
```python
# ✅ Good - Load from environment
OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')

# ❌ Bad - Hardcoded in code
OPENAI_API_KEY = "sk-proj-your-actual-key"
```

#### 3. **File Permissions**
- Set proper permissions on `.env` file: `chmod 600 .env` (Unix/Linux)
- Keep `.env` file in project root only
- Don't share `.env` file via email/chat

#### 4. **Production Deployment**
- Use environment variables in production
- Consider using secret management services
- Rotate API keys regularly
- Monitor API usage for unusual activity

### 🔍 **How to Check if Your API Key is Secure**

1. **Check git status**: `git status` should not show `.env`
2. **Search codebase**: No hardcoded keys in source files
3. **Review commits**: No API keys in git history
4. **Environment loading**: App loads key from environment only

### 🆘 **If API Key is Compromised**

1. **Immediately disable** the key in OpenAI dashboard
2. **Generate a new** API key
3. **Update** your `.env` file with new key
4. **Review** recent API usage for unauthorized calls
5. **Check** git history and remove any exposed keys

### 📋 **Security Checklist**

- [x] API key removed from source code
- [x] API key stored in `.env` file
- [x] `.env` file added to `.gitignore`
- [x] Environment variable validation added
- [x] Example file created for setup guidance
- [ ] Regular API key rotation scheduled
- [ ] API usage monitoring enabled

## Environment Setup

### Required Environment Variables
```env
OPENAI_API_KEY=your_actual_openai_api_key
SECRET_KEY=your_random_secret_key
FLASK_ENV=development
DATABASE_URL=sqlite:///chatbot.db
PORT=5000
```

### Setup Instructions
1. Copy `.env.example` to `.env`
2. Replace placeholder values with actual keys
3. Never commit `.env` to version control
4. Keep API keys confidential
