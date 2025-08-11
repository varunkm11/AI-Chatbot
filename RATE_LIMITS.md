# 🚦 Rate Limiting Guide

## 🔍 **Why Rate Limits Happen**

OpenAI has rate limits to prevent abuse and ensure fair usage:

### **Common Rate Limits:**
- **Requests per minute (RPM)**: Free tier ~3-20 RPM
- **Tokens per minute (TPM)**: Varies by model and tier
- **Daily limits**: Based on your usage tier

## ⚡ **Improvements Made**

### **1. Automatic Retry Logic**
- **3 retry attempts** with exponential backoff
- **Smart delays**: 1s, 2s, 4s + random jitter
- **Console logging** to track retry attempts

### **2. Better Error Messages**
- **Helpful suggestions** for rate limit errors
- **Wait time recommendations**
- **Model switching suggestions**

### **3. Enhanced Configuration**
```python
# New settings in config.py
RATE_LIMIT_REQUESTS = 20     # Reduced from 100
MIN_REQUEST_INTERVAL = 2     # Minimum 2s between requests
MAX_RETRIES = 3              # Automatic retry attempts
```

## 🛠️ **How to Avoid Rate Limits**

### **1. Wait Between Messages**
- **Minimum**: 2-3 seconds between requests
- **Recommended**: 5-10 seconds for heavy usage
- **Free tier**: Wait 1-2 minutes between requests

### **2. Choose Efficient Models**
- **Best**: `gpt-3.5-turbo` (fastest, cheapest)
- **Moderate**: `gpt-4o-mini` (balanced)
- **Avoid**: `gpt-4` for frequent requests (slower)

### **3. Optimize Usage**
- **Shorter messages** = fewer tokens = faster processing
- **Clear conversation history** regularly
- **Use concise prompts**

## 🔧 **If You Still Get Rate Limited**

### **Immediate Solutions:**
1. **Wait 1-2 minutes** before next request
2. **Switch to GPT-3.5-turbo** (faster processing)
3. **Refresh the page** to start new session
4. **Check your OpenAI usage** at platform.openai.com

### **Long-term Solutions:**
1. **Upgrade OpenAI plan** for higher limits
2. **Add credits** to your account
3. **Monitor usage** in OpenAI dashboard
4. **Consider usage patterns** (avoid burst requests)

## 📊 **OpenAI Rate Limits by Tier**

### **Free Tier ($0)**
- **GPT-3.5-turbo**: 3 RPM, 40,000 TPM
- **GPT-4**: 3 RPM, 150,000 TPM
- **Daily limits**: $100/month usage cap

### **Tier 1 ($5+ spent)**
- **GPT-3.5-turbo**: 3,500 RPM, 90,000 TPM
- **GPT-4**: 500 RPM, 30,000 TPM
- **Higher daily limits**

### **Tier 2+ ($50+ spent)**
- **Even higher limits**
- **Priority access**
- **Better performance**

## 🎯 **Best Practices**

1. **Test with GPT-3.5-turbo first** (most forgiving limits)
2. **Add a small delay** between consecutive requests
3. **Monitor your usage** in OpenAI dashboard
4. **Start with smaller conversations** to test limits
5. **Consider upgrading** if you need frequent access

## 🆘 **Troubleshooting**

### **"Rate Limited" Error:**
- Wait 60 seconds and try again
- Switch to GPT-3.5-turbo model
- Check if you have API credits

### **"Insufficient Credits" Error:**
- Add credits at platform.openai.com/billing
- Minimum $5 recommended for testing

### **"API Key Error:**
- Verify API key in .env file
- Check key permissions in OpenAI dashboard

## 📝 **Current Status**

✅ **Automatic retries implemented**
✅ **Exponential backoff added**
✅ **Better error messages**
✅ **Rate limit configuration updated**
✅ **Console logging for debugging**

Your chatbot now handles rate limits much better and will automatically retry failed requests!
