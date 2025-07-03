@echo off
echo 🤖 Advanced AI Chatbot - Setup Script
echo.

echo Installing Python dependencies...
pip install -r requirements.txt

echo.
echo Creating environment file...
if not exist .env (
    copy .env.example .env
    echo Please edit .env file with your OpenRouter API key
)

echo.
echo Setup complete! Choose how to run:
echo.
echo 1. FastAPI (Recommended for production)
echo    python fastapi_chatbot.py
echo.
echo 2. Flask (Simple and lightweight)
echo    python flask_chatbot.py
echo.
echo 3. Streamlit (Interactive web app)
echo    streamlit run advanced_chatbot.py
echo.
echo For website integration, see demo.html
echo.
pause
