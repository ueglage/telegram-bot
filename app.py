from flask import Flask, request
from telegram import Bot, Update
import os

BOT_TOKEN = "7252963844:AAELhpxerpcaYXiff2ktagQORfMJ44ZA1Hs"
GROUP_CHAT_ID = "-1002517942232"  # ID вашої групи

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

# Повідомлення привітання та інформації про бота
WELCOME_MESSAGE = """
Привіт, вітаю! 👋 Я бот, який вміє пересилати файли в Медійну групу до операторів. Просто перешліть мені будь-який файл (фото, відео, документ, аудіо чи голосове повідомлення) і я його їм перешлю.
"""

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    handle_update(update)
    return "OK"

def handle_update(update):
    msg = update.effective_message

    if msg: # Перевіряємо, чи є повідомлення
        if msg.text == "/start":
            # Відправляємо привітання тільки при команді /start
            bot.send_message(chat_id=msg.chat_id, text=WELCOME_MESSAGE)
        elif msg.document:
            bot.send_document(chat_id=GROUP_CHAT_ID, document=msg.document.file_id, caption=msg.caption)
            bot.send_message(chat_id=msg.chat_id, text="Файл успішно переслано!")
        elif msg.photo:
            # Telegram API може повертати кілька розмірів фото, беремо останній (найбільший)
            bot.send_photo(chat_id=GROUP_CHAT_ID, photo=msg.photo[-1].file_id, caption=msg.caption)
            bot.send_message(chat_id=msg.chat_id, text="Фото успішно переслано!")
        elif msg.video:
            bot.send_video(chat_id=GROUP_CHAT_ID, video=msg.video.file_id, caption=msg.caption)
            bot.send_message(chat_id=msg.chat_id, text="Відео успішно переслано!")
        elif msg.audio:
            bot.send_audio(chat_id=GROUP_CHAT_ID, audio=msg.audio.file_id, caption=msg.caption)
            bot.send_message(chat_id=msg.chat_id, text="Аудіо успішно переслано!")
        elif msg.voice:
            bot.send_voice(chat_id=GROUP_CHAT_ID, voice=msg.voice.file_id)
            bot.send_message(chat_id=msg.chat_id, text="Голосове повідомлення успішно переслано!")
        elif msg.text: # Ігноруємо будь-який інший текст, що не є командою /start
            bot.send_message(chat_id=msg.chat_id, text="Я можу пересилати лише *файли* (фото, відео, документ, аудіо чи голосове повідомлення). Будь ласка, надішліть мені файл.", parse_mode="Markdown")

@app.route('/')
def home():
    return '🤖 Bot is running!'

