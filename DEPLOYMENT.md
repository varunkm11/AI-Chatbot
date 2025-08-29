# AI Chatbot - Deployment Guide

## Deploy to Vercel

This application is configured for deployment on Vercel. Follow these steps:

### Prerequisites
1. Install Vercel CLI: `npm install -g vercel`
2. Create a Vercel account at [vercel.com](https://vercel.com)
3. Have your API keys ready (OpenRouter or OpenAI)

### Deployment Steps

1. **Login to Vercel**
   ```bash
   vercel login
   ```

2. **Deploy from project directory**
   ```bash
   vercel --prod
   ```

3. **Set Environment Variables**
   In your Vercel dashboard or using CLI:
   ```bash
   vercel env add SECRET_KEY
   vercel env add API_PROVIDER
   vercel env add OPENROUTER_API_KEY
   # or
   vercel env add OPENAI_API_KEY
   ```

### Environment Variables

Set these in your Vercel dashboard:

- `SECRET_KEY`: A random secret key for Flask sessions
- `API_PROVIDER`: Either `openai` or `openrouter`
- `OPENROUTER_API_KEY`: Your OpenRouter API key (if using OpenRouter)
- `OPENAI_API_KEY`: Your OpenAI API key (if using OpenAI)
- `DATABASE_URL`: PostgreSQL connection string (optional, defaults to SQLite)

### Database Considerations

- **Development**: Uses SQLite (local file)
- **Production**: Configure PostgreSQL for persistent data storage
- **Serverless**: SQLite files don't persist between function invocations

For production, consider using:
- PostgreSQL (Supabase, Railway, etc.)
- MongoDB Atlas
- Firebase Firestore

### Post-Deployment

1. Visit your deployed URL
2. Test the chat functionality
3. Monitor logs in Vercel dashboard

### Local Development

1. Copy `.env.example` to `.env`
2. Fill in your API keys
3. Run: `python app.py`

### Troubleshooting

- Check Vercel function logs for errors
- Ensure all environment variables are set
- Verify API keys are valid
- Database connection issues: Check DATABASE_URL
