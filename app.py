from flask import Flask, request 
from telegram import Bot, Update, User # Додано User для типізації
import os

BOT_TOKEN = "7252963844:AAGrjzhKVDt0IGW6k2pNxZM2ntJO8PPjMB8" # Ваш токен
GROUP_CHAT_ID = "-1002517942232"  # ID вашої групи

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

# Повідомлення привітання та інформації про бота
WELCOME_MESSAGE = """
Привіт, вітаю! 👋 Я бот, який вміє пересилати файли в Медійну групу до операторів. Просто перешліть мені будь-який файл (фото, відео, документ, аудіо чи голосове повідомлення) і я його їм перешлю.
"""

def get_sender_info(user: User) -> str:
    """Формує рядок з інформацією про відправника."""
    info_parts = [f"Ім'я: {user.first_name}"]
    if user.username:
        info_parts.append(f"Username: @{user.username}")
    info_parts.append(f"ID: {user.id}")
    return "Інформація про відправника:\n" + "\n".join(info_parts) + "\n\n"

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    handle_update(update)
    return "OK"

def handle_update(update: Update):
    msg = update.effective_message

    if msg: # Перевіряємо, чи є повідомлення
        sender_info_text = ""
        if msg.from_user: # Отримуємо інформацію, якщо є відправник
            sender_info_text = get_sender_info(msg.from_user)

        if msg.text == "/start":
            # Відправляємо привітання тільки при команді /start
            bot.send_message(chat_id=msg.chat_id, text=WELCOME_MESSAGE)
        elif msg.document:
            caption = sender_info_text + (msg.caption if msg.caption else "")
            bot.send_document(chat_id=GROUP_CHAT_ID, document=msg.document.file_id, caption=caption)
            bot.send_message(chat_id=msg.chat_id, text="Файл успішно переслано!")
        elif msg.photo:
            caption = sender_info_text + (msg.caption if msg.caption else "")
            # Telegram API може повертати кілька розмірів фото, беремо останній (найбільший)
            bot.send_photo(chat_id=GROUP_CHAT_ID, photo=msg.photo[-1].file_id, caption=caption)
            bot.send_message(chat_id=msg.chat_id, text="Фото успішно переслано!")
        elif msg.video:
            caption = sender_info_text + (msg.caption if msg.caption else "")
            bot.send_video(chat_id=GROUP_CHAT_ID, video=msg.video.file_id, caption=caption)
            bot.send_message(chat_id=msg.chat_id, text="Відео успішно переслано!")
        elif msg.audio:
            caption = sender_info_text + (msg.caption if msg.caption else "")
            bot.send_audio(chat_id=GROUP_CHAT_ID, audio=msg.audio.file_id, caption=caption)
            bot.send_message(chat_id=msg.chat_id, text="Аудіо успішно переслано!")
        elif msg.voice:
            # Голосові повідомлення також можуть мати caption
            caption = sender_info_text # Для голосових можна просто інформацію про відправника
            bot.send_voice(chat_id=GROUP_CHAT_ID, voice=msg.voice.file_id, caption=caption)
            bot.send_message(chat_id=msg.chat_id, text="Голосове повідомлення успішно переслано!")
        elif msg.text: # Ігноруємо будь-який інший текст, що не є командою /start
            bot.send_message(chat_id=msg.chat_id, text="Я можу пересилати лише *файли* (фото, відео, документ, аудіо чи голосове повідомлення). Будь ласка, надішліть мені файл.", parse_mode="Markdown")

@app.route('/')
def home():
    return '🤖 Bot is running!'

# Для локального запуску та тестування (необов'язково для деплою на сервері, що підтримує WSGI)
# if __name__ == "__main__":
#     # Важливо: для продакшену використовуйте більш надійний WSGI сервер, наприклад Gunicorn
#     # Замініть 'YOUR_PUBLIC_IP_OR_DOMAIN' на вашу публічну IP адресу або домен, якщо налаштовуєте вебхук вручну
#     # bot.set_webhook(f"https://YOUR_PUBLIC_IP_OR_DOMAIN/{BOT_TOKEN}")
#     app.run(host="0.0.0.0", port=int(os.environ.get('PORT', 8080)))
