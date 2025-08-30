# Render Deployment Guide for AI Chatbot

This guide will help you deploy your AI Chatbot to Render.com

## Prerequisites

1. **Render Account**: Create a free account at [render.com](https://render.com)
2. **GitHub Repository**: Your code should be in a GitHub repository
3. **OpenRouter API Key**: Your API key from OpenRouter

## Deployment Steps

### 1. Prepare Your Repository

Ensure your repository has these files (already created):
- `requirements.txt` - Python dependencies
- `render.yaml` - Render service configuration
- `build.sh` - Build script for Render
- `Procfile` - Process file (alternative to render.yaml)
- `.env` - Environment variables (for local development only)

### 2. Connect to Render

1. Log in to your Render dashboard
2. Click **"New +"** → **"Web Service"**
3. Connect your GitHub repository
4. Select your AI-Chatbot repository

### 3. Configure Service Settings

**Basic Settings:**
- **Name**: `ai-chatbot` (or your preferred name)
- **Environment**: `Python 3`
- **Region**: Choose closest to your users
- **Branch**: `main`

**Build Settings:**
- **Build Command**: `./build.sh` (or leave empty to use render.yaml)
- **Start Command**: `gunicorn --bind 0.0.0.0:$PORT app:app`

### 4. Environment Variables

Add these environment variables in Render dashboard:

**Required:**
- `OPENROUTER_API_KEY`: Your OpenRouter API key
- `FLASK_ENV`: `production`
- `SECRET_KEY`: Generate a random secret key

**Optional:**
- `OPENROUTER_MODEL`: Specific model (default: meta-llama/llama-3.1-8b-instruct:free)
- `PYTHON_VERSION`: `3.11.0`

### 5. Database Setup

**Option 1: Using render.yaml (Recommended)**
The included `render.yaml` file will automatically create a PostgreSQL database.

**Option 2: Manual Database Creation**
1. Create a new PostgreSQL database in Render
2. Copy the **Internal Database URL**
3. Add it as `DATABASE_URL` environment variable

### 6. Deploy

1. Click **"Create Web Service"**
2. Render will automatically:
   - Install dependencies from `requirements.txt`
   - Run the build script
   - Start your application with gunicorn

### 7. Post-Deployment

1. **Check Logs**: Monitor the deployment logs for any errors
2. **Test Application**: Visit your Render URL to test the chatbot
3. **Database**: The database will be automatically initialized on first run

## Environment Variables Reference

```bash
# Required
OPENROUTER_API_KEY=your_openrouter_api_key_here
FLASK_ENV=production

# Optional
SECRET_KEY=your_secret_key_here
OPENROUTER_MODEL=meta-llama/llama-3.1-8b-instruct:free
DATABASE_URL=postgresql://... # Auto-set by Render if using PostgreSQL
```

## Troubleshooting

### Common Issues:

1. **Build Fails**: Check that all dependencies in `requirements.txt` are correct
2. **App Crashes**: Check logs for Python errors, usually related to missing environment variables
3. **Database Errors**: Ensure DATABASE_URL is set correctly
4. **API Errors**: Verify your OpenRouter API key is valid

### Checking Logs:
- Go to your service dashboard in Render
- Click on **"Logs"** tab to see real-time logs

## Production Considerations

1. **Database Backups**: Enable automatic backups in Render PostgreSQL settings
2. **Scaling**: Render will auto-scale based on your plan
3. **Domain**: You can add a custom domain in service settings
4. **SSL**: Render provides free SSL certificates automatically

## Local Development vs Production

- **Local**: Uses SQLite database, Flask development server
- **Production**: Uses PostgreSQL database, Gunicorn WSGI server

## Support

If you encounter issues:
1. Check Render documentation: https://render.com/docs
2. Review application logs in Render dashboard
3. Ensure all environment variables are properly set

## Cost

- **Web Service**: Free tier available (with limitations)
- **PostgreSQL**: Free tier includes 1GB storage
- **Paid Plans**: Available for production workloads

Your AI Chatbot should now be successfully deployed on Render! 🎉
