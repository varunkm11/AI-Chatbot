# 🚀 Heroku Deployment Guide for Advanced AI Chatbot

## Prerequisites
1. **Heroku Account**: Sign up at https://heroku.com
2. **Heroku CLI**: Install from https://devcenter.heroku.com/articles/heroku-cli
3. **Git**: Make sure Git is installed on your system

## 📁 Files Created for Heroku Deployment

### Required Files:
- `Procfile` - Tells Heroku how to run your app
- `setup.sh` - Configures Streamlit for Heroku
- `runtime.txt` - Specifies Python version
- `requirements-heroku.txt` - Minimal dependencies for Heroku
- `heroku_chatbot.py` - Heroku-optimized version of the chatbot

## 🛠️ Step-by-Step Deployment

### 1. Install Heroku CLI
```bash
# Windows (using installer from heroku.com)
# macOS
brew tap heroku/brew && brew install heroku
# Ubuntu
sudo snap install --classic heroku
```

### 2. Login to Heroku
```bash
heroku login
```

### 3. Initialize Git Repository (if not already done)
```bash
git init
git add .
git commit -m "Initial commit"
```

### 4. Create Heroku App
```bash
# Replace 'your-chatbot-name' with your desired app name
heroku create your-chatbot-name
```

### 5. Set Environment Variables
```bash
# Set your OpenRouter API key
heroku config:set OPENROUTER_API_KEY=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
```

### 6. Copy Requirements File
```bash
# Use the Heroku-specific requirements
cp requirements-heroku.txt requirements.txt
```

### 7. Update Procfile for Heroku Version
```bash
echo "web: sh setup.sh && streamlit run heroku_chatbot.py --server.port=\$PORT --server.address=0.0.0.0" > Procfile
```

### 8. Deploy to Heroku
```bash
git add .
git commit -m "Deploy to Heroku"
git push heroku main
```

### 9. Open Your App
```bash
heroku open
```

## 🔧 Configuration Files Explanation

### `Procfile`
```
web: sh setup.sh && streamlit run heroku_chatbot.py --server.port=$PORT --server.address=0.0.0.0
```

### `setup.sh`
```bash
mkdir -p ~/.streamlit/

echo "\
[general]\n\
email = \"your-email@domain.com\"\n\
" > ~/.streamlit/credentials.toml

echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = \$PORT\n\
" > ~/.streamlit/config.toml
```

### `runtime.txt`
```
python-3.9.18
```

## 🌐 Environment Variables

Set these in Heroku Dashboard or via CLI:

```bash
# Required
heroku config:set OPENROUTER_API_KEY=your_api_key_here

# Optional (for additional features)
heroku config:set OPENWEATHER_API_KEY=your_weather_api_key
heroku config:set NEWS_API_KEY=your_news_api_key
```

## 🔍 Troubleshooting

### Common Issues and Solutions:

1. **Build Failed - Dependencies**
   ```bash
   # Check your requirements.txt
   heroku logs --tail
   ```

2. **App Crashes - Port Issues**
   ```bash
   # Make sure Procfile uses $PORT variable
   heroku logs --tail
   ```

3. **API Key Not Working**
   ```bash
   # Check environment variables
   heroku config
   ```

4. **Streamlit Not Loading**
   ```bash
   # Check setup.sh permissions
   chmod +x setup.sh
   ```

## 📊 Monitoring Your App

### View Logs
```bash
heroku logs --tail
```

### Check App Status
```bash
heroku ps
```

### Restart App
```bash
heroku restart
```

## 💰 Heroku Pricing

- **Free Tier**: 550-1000 dyno hours/month (app sleeps after 30 min inactivity)
- **Hobby Tier**: $7/month (app doesn't sleep)
- **Professional**: $25+/month (more resources)

## 🚀 Scaling Your App

### Scale Up
```bash
# Upgrade to hobby dyno (no sleeping)
heroku ps:scale web=1 --type=hobby

# Scale to professional
heroku ps:scale web=1 --type=standard-1x
```

## 🔒 Security Best Practices

1. **Never commit API keys** to Git
2. **Use environment variables** for sensitive data
3. **Enable HTTPS** (automatic on Heroku)
4. **Regular updates** of dependencies

## 📱 Custom Domain (Optional)

```bash
# Add your domain
heroku domains:add www.your-domain.com

# Configure DNS
# Add CNAME record: www -> your-app-name.herokuapp.com
```

## 🎯 Quick Deploy Commands

Create this script as `deploy.sh`:

```bash
#!/bin/bash
echo "🚀 Deploying to Heroku..."

# Copy Heroku requirements
cp requirements-heroku.txt requirements.txt

# Add files to git
git add .
git commit -m "Deploy: $(date)"

# Push to Heroku
git push heroku main

echo "✅ Deployment complete!"
echo "🌐 Your app: https://your-chatbot-name.herokuapp.com"
```

Make it executable:
```bash
chmod +x deploy.sh
./deploy.sh
```

## 🌟 Features Available in Heroku Deployment

✅ **Core Chatbot Functionality**
✅ **Multiple AI Models** 
✅ **Real-time Data** (if dependencies installed)
✅ **Chat History Export**
✅ **System Prompt Customization**
✅ **Responsive Design**
✅ **Environment Variable Configuration**

## 📞 Support

If you encounter issues:

1. Check Heroku logs: `heroku logs --tail`
2. Verify environment variables: `heroku config`
3. Check app status: `heroku ps`
4. Review Heroku documentation: https://devcenter.heroku.com

Your chatbot will be accessible at: `https://your-app-name.herokuapp.com`

Happy deploying! 🎉
