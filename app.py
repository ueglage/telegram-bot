from flask import Flask, request
from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton, ParseMode
import os

BOT_TOKEN = "7252963844:AAELhpxerpcaYXiff2ktagQORfMJ44ZA1Hs"
GROUP_CHAT_ID = "-1002517942232"  # ID вашої групи

bot = Bot(token=BOT_TOKEN)
app = Flask(__name__)

# Дані для меню
ABOUT_US_TEXT = """
Ми - українська громада християн у Німеччині, яка об'єднана любов'ю до Бога та бажанням служити один одному. Церква, в якій Бог змінює життя. Тут кожен може знайти підтримку, надію та любов.

*Що робимо?*
Проповідуємо Євангеліє - добру звістку про спасіння через Ісуса Христа.
Молимось разом - за родини, Україну, мир, зцілення і потреби людей.
Підтримуємо одне одного - духовно, емоційно та практично.
Організовуємо зустрічі для молоді, дітей, жінок та чоловіків.

*Наше бачення*
Церква - це не будівля, а люди.
Любов - це мова, яку розуміє кожен.
Віра - це шлях, на якому ніхто не має йти наодинці.
Відкрий серце для чогось більшого. Ми раді тобі незалежно від віку, досвіду чи минулого.
"""

SCHEDULE_TEXT = """
*Розклад зібрань та заходів*
Зібрання: Щонеділі о 12:30
Молодіжні спілкування: Щонеділі о 17:00
Підліткові TEENY LAGE: Субота о 16:00
Розбір Слова Божого: Щочетверга о 19:00
Волейбол (Спортивне служіння для молоді): Щосeреди о 18:00
"""

CONTACTS_TEXT = """
*Контакти*
*Телефони:*
*Віктор:*
+49 151 2050 3835 (WhatsApp)
+380 96 811 3453 (Viber)
*Михайло:*
+380 97 940 0603 (Viber)
*Петро:*
+49 151 7281 2211 (WhatsApp)
+380 50 493 9608 (Viber)

*Адреса:*
Feldstraße 53, 32791 Lage

*Ми в соціальних мережах:*
YouTube: @ueglage 
Instagram: @ueglage
Telegram Bot: @ueglage_bot
"""

WELCOME_MESSAGE = """
Привіт, вітаю! 👋 Я бот, який вміє пересилати файли в Медійну групу до операторів. Просто перешліть мені файл (фото, відео, документ, аудіо чи голосове повідомлення) і я його їм перешлю.
"""

BOT_INFO_MESSAGE = """
Я бот, створений для зручного пересилання медіафайлів (фото, відео, документи, аудіо, голосові повідомлення) до медійної групи операторів. Це спрощує обмін файлами та допомагає зберегти порядок у груповому чаті.
Просто надішліть мені потрібний файл, і я автоматично перешлю його до групи.
"""

# Функція для створення інлайн-клавіатури
def get_main_menu_keyboard():
    keyboard = [
        [InlineKeyboardButton("1. Старт", callback_data="start")],
        [InlineKeyboardButton("2. Про нас", callback_data="about_us")],
        [InlineKeyboardButton("3. Розклад служінь", callback_data="schedule")],
        [InlineKeyboardButton("4. Контакти церкви", callback_data="contacts")]
    ]
    return InlineKeyboardMarkup(keyboard)

@app.route(f"/{BOT_TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), bot)
    handle_update(update)
    return "OK"

def handle_update(update):
    msg = update.effective_message
    query = update.callback_query

    # Обробка команд і текстових повідомлень
    if msg:
        if msg.text == "/start":
            bot.send_message(chat_id=msg.chat_id, text=WELCOME_MESSAGE, reply_markup=get_main_menu_keyboard())
        elif msg.text and msg.text.startswith('/'): # Ігноруємо інші текстові команди
            pass
        elif msg.document:
            bot.send_document(chat_id=GROUP_CHAT_ID, document=msg.document.file_id, caption=msg.caption)
            bot.send_message(chat_id=msg.chat_id, text="Файл успішно переслано!")
        elif msg.photo:
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
        elif msg.text: # Ігноруємо всі інші текстові повідомлення, які не є командами
            bot.send_message(chat_id=msg.chat_id, text="Будь ласка, перешліть мені *файл* (фото, відео, документ, аудіо чи голосове повідомлення). Я не пересилаю текстові повідомлення в медійну групу. Для взаємодії скористайтеся меню.", parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu_keyboard())


    # Обробка натискань на кнопки меню
    elif query:
        chat_id = query.message.chat_id
        message_id = query.message.message_id

        if query.data == "start":
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=BOT_INFO_MESSAGE, reply_markup=get_main_menu_keyboard())
        elif query.data == "about_us":
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=ABOUT_US_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu_keyboard())
        elif query.data == "schedule":
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=SCHEDULE_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu_keyboard())
        elif query.data == "contacts":
            bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=CONTACTS_TEXT, parse_mode=ParseMode.MARKDOWN, reply_markup=get_main_menu_keyboard())

        bot.answer_callback_query(query.id) # Важливо відповісти на callback_query


@app.route('/')
def home():
    return '🤖 Bot is running!'

