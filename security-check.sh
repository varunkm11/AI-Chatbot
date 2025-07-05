#!/bin/bash
# API Key Security Check Script

echo "🔍 API Key Security Audit"
echo "========================"

# Check if .env is tracked
echo "1. Checking if .env is tracked by Git..."
if git ls-files --error-unmatch .env >/dev/null 2>&1; then
    echo "❌ CRITICAL: .env is tracked by Git!"
else
    echo "✅ .env is not tracked"
fi

# Check if .env is ignored
echo "2. Checking if .env is properly ignored..."
if git check-ignore .env >/dev/null 2>&1; then
    echo "✅ .env is properly ignored"
else
    echo "❌ WARNING: .env is not ignored"
fi

# Check for API keys in commit history
echo "3. Checking commit history for API keys..."
if git log --all --grep="API" --grep="key" --grep="secret" -i --oneline | head -5; then
    echo "⚠️  Found commits mentioning API/keys - review manually"
else
    echo "✅ No obvious API key commits found"
fi

# Check for sensitive patterns in tracked files
echo "4. Checking tracked files for sensitive patterns..."
if git grep -i "api.key\|secret\|password\|token" -- '*.py' '*.js' '*.html' '*.json'; then
    echo "⚠️  Found potential sensitive data in tracked files"
else
    echo "✅ No sensitive patterns found in tracked files"
fi

echo "========================"
echo "🔒 Security audit complete"
