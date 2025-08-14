# 🚀 API Setup Guide - Fix Rate Limiting

## 🎯 **Best APIs to Avoid Rate Limits**

### **1. OpenRouter (Recommended) 🌟**
- **Free models available** (no rate limits!)
- **Access to multiple AI providers** (OpenAI, Anthropic, Google, Meta)
- **Better rate limits** than direct OpenAI
- **Cheaper than OpenAI direct**

#### Setup OpenRouter:
1. Go to https://openrouter.ai/
2. Sign up for free account
3. Get your API key from dashboard
4. Update `.env` file:
   ```env
   API_PROVIDER=openrouter
   OPENROUTER_API_KEY=sk-or-v1-your-key-here
   ```

### **2. Groq API (Very Fast) ⚡**
- **Generous free tier** (6000 requests/day)
- **Ultra-fast responses** (10x faster than OpenAI)
- **Good model selection**

#### Setup Groq:
1. Go to https://groq.com/
2. Sign up and get API key
3. Update `.env` file:
   ```env
   API_PROVIDER=groq
   GROQ_API_KEY=gsk_your-key-here
   ```

### **3. Keep OpenAI as Backup**
Your current OpenAI key will work as fallback

## 🔧 **Quick Fix Steps**

### **Step 1: Get OpenRouter Key (Easiest)**
1. **Visit**: https://openrouter.ai/
2. **Sign up** (free)
3. **Get API key** from dashboard
4. **Replace** in `.env` file:
   ```env
   OPENROUTER_API_KEY=your_actual_key_here
   ```

### **Step 2: Update Environment**
Your `.env` file should look like:
```env
API_PROVIDER=openrouter
OPENROUTER_API_KEY=sk-or-v1-your-actual-key
OPENAI_API_KEY=your-openai-key-as-backup
```

### **Step 3: Restart Server**
```bash
python app.py
```

## 🆓 **Free Models Available**

With OpenRouter, you get these **completely free** models:
- **Llama 3.1 8B** (Meta) - No rate limits!
- **Mistral 7B** - Fast and capable
- **Phi-3 Mini** (Microsoft) - Efficient
- **Gemma 7B** (Google) - Good performance

## 💰 **Cost Comparison**

| Provider | Free Tier | Rate Limits | Cost |
|----------|-----------|-------------|------|
| **OpenRouter** | ✅ Free models | ❌ None for free | 50% cheaper |
| **Groq** | ✅ 6000/day | ⚠️ Daily limit | Free tier generous |
| **OpenAI Direct** | ❌ Limited | 🚫 Strict | Most expensive |

## 🎯 **Immediate Solution**

**Right now, to fix your rate limiting:**

1. **Use OpenRouter** (recommended)
   - Sign up at https://openrouter.ai/
   - Get free API key
   - Use free models (no limits!)

2. **Or use Groq** (fastest)
   - Sign up at https://groq.com/
   - Get free API key
   - 6000 requests/day free

3. **Or wait 1-2 hours** (OpenAI limits reset)

## 🔄 **Your App is Ready**

Your chatbot is now configured to support:
- ✅ **Multiple API providers**
- ✅ **Automatic switching**
- ✅ **Free model options**
- ✅ **Better rate limit handling**

Just get an API key from OpenRouter or Groq and update your `.env` file!

## 📝 **Current Status**

- **API Provider**: Set to `openrouter` (best option)
- **Default Model**: Llama 3.1 8B Free (no rate limits)
- **Backup**: Your OpenAI key still works
- **Models**: Free and paid options available

**Get your OpenRouter key and you'll never hit rate limits again!** 🚀
