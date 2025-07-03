@echo off
echo 🚀 Preparing for Heroku deployment...

echo 📦 Copying Heroku requirements...
copy requirements-heroku.txt requirements.txt

echo 📝 Updating Procfile...
echo web: sh setup.sh ^&^& streamlit run heroku_chatbot.py --server.port=$PORT --server.address=0.0.0.0 > Procfile

echo ✅ Ready for Heroku deployment!
echo.
echo Next steps:
echo 1. heroku create your-app-name
echo 2. heroku config:set OPENROUTER_API_KEY=your_api_key
echo 3. git add .
echo 4. git commit -m "Deploy to Heroku"
echo 5. git push heroku main
echo 6. heroku open
echo.
echo 📚 See HEROKU_DEPLOYMENT.md for detailed instructions
pause
