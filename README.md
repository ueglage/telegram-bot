# Telegram Bot Flask (у Render)

## 🔧 Інструкція

1. Зайди на https://render.com
2. Створи акаунт (або увійди)
3. Натисни **"New" → "Web Service"**
4. Підключи свій GitHub або завантаж ZIP вручну
5. У налаштуваннях:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn app:app`
   - Environment:
     - BOT_TOKEN = твій токен від BotFather
     - GROUP_CHAT_ID = -100... (ідентифікатор групи)
6. Після запуску Render покаже тобі URL.

7. В браузері відкрий посилання:
```
https://api.telegram.org/bot<ТВІЙ_ТОКЕН>/setWebhook?url=https://назва-проєкту.onrender.com/<ТВІЙ_ТОКЕН>
```

✅ Все, бот працює!