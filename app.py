from flask import Flask, request
from telegram import Bot, Update
import os

BOT_TOKEN = os.environ.get("BOT_TOKEN")
GROUP_CHAT_ID = os.environ.get("GROUP_CHAT_ID")

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    handle_update(update)
    return "OK"

def handle_update(update):
    msg = update.effective_message

    if msg.document:
        bot.send_document(chat_id=GROUP_CHAT_ID, document=msg.document.file_id, caption=msg.caption)
    elif msg.photo:
        bot.send_photo(chat_id=GROUP_CHAT_ID, photo=msg.photo[-1].file_id, caption=msg.caption)
    elif msg.video:
        bot.send_video(chat_id=GROUP_CHAT_ID, video=msg.video.file_id, caption=msg.caption)
    elif msg.audio:
        bot.send_audio(chat_id=GROUP_CHAT_ID, audio=msg.audio.file_id, caption=msg.caption)
    elif msg.voice:
        bot.send_voice(chat_id=GROUP_CHAT_ID, voice=msg.voice.file_id)
    elif msg.text:
        bot.send_message(chat_id=GROUP_CHAT_ID, text=msg.text)

@app.route('/')
def home():
    return '🤖 Bot is running!'

# 🟢 ВАЖЛИВО: запуск Flask сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
