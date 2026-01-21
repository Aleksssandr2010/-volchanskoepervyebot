import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

TOKEN = os.getenv("TOKEN")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
COUNTER_FILE = os.path.join(BASE_DIR, "secret_counter.txt")  # файл для счётчика

# ----------- МЕНЮ -----------
def main_menu():
    keyboard = [
        [
            InlineKeyboardButton("ℹ️ О нас", callback_data="img1"),
            InlineKeyboardButton("👤 Как вступить?", callback_data="img2"),
        ],
        [
            InlineKeyboardButton("🎯 Направления", callback_data="img3"),
            InlineKeyboardButton("🎁 Что вы получите", callback_data="img4"),
        ],
        [
            InlineKeyboardButton("🏗 Структура", callback_data="img5"),
            InlineKeyboardButton("📅 Календарь", callback_data="img6"),
        ],
        [
            InlineKeyboardButton("🔗 Полезные ссылки", callback_data="img7"),
            InlineKeyboardButton("❓ FAQ", callback_data="img8"),
        ],
        [
            InlineKeyboardButton("📞 Контакты", callback_data="img9"),
            InlineKeyboardButton("✍️ Обратная связь", callback_data="img10"),
        ],
    ]
    return InlineKeyboardMarkup(keyboard)

def back_menu():
    keyboard = [[InlineKeyboardButton("⬅ Назад в меню", callback_data="back")]]
    return InlineKeyboardMarkup(keyboard)

# ----------- УДАЛЕНИЕ СТАРЫХ СООБЩЕНИЙ -----------
async def clear_last(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
    last_id = context.user_data.get("last_bot_message")
    if last_id:
        try:
            await context.bot.delete_message(chat_id=chat_id, message_id=last_id)
        except:
            pass

# ----------- СЧЁТЧИК СЕКРЕТА -----------
def read_counter():
    try:
        with open(COUNTER_FILE, "r") as f:
            return int(f.read())
    except:
        return 0

def write_counter(count):
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))

# ----------- /start -----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    await clear_last(context, chat_id)

    msg = await update.message.reply_text(
        "📌 *Цифровой навигатор первичного отделения «Движения Первых» Волчанской школы*\n\n"
        "Выберите интересующий раздел:",
        reply_markup=main_menu(),
        parse_mode="Markdown"
    )

    context.user_data["last_bot_message"] = msg.message_id

# ----------- КНОПКИ -----------
async def buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    chat_id = query.message.chat_id
    await query.answer()

    await clear_last(context, chat_id)

    images = {
        "img1": ("img1inf.png", "ℹ️ *О нас*"),
        "img2": ("img2who.png", "👤 *Как вступить?*"),
        "img3": ("img3trai.png", "🎯 *Направления деятельности*"),
        "img4": ("img4bonus.png", "🎁 *Что вы получите*"),
        "img5": ("img5structur.png", "🏗 *Структура отделения*"),
        "img6": ("img6calendar.png", "📅 *Календарь событий*"),
        "img7": ("img7link.png", "🔗 *Полезные ссылки*"),
        "img8": ("img8faq.png", "❓ *Часто задаваемые вопросы*"),
        "img9": ("img9contact.png", "📞 *Наши контакты*"),
        "img10": ("img10feedback.png", "✍️ *Обратная связь*"),
    }

    if query.data == "back":
        msg = await query.message.reply_text(
            "📌 *Главное меню*",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
        context.user_data["last_bot_message"] = msg.message_id
        return

    if query.data in images:
        file_name, caption = images[query.data]
        file_path = os.path.join(BASE_DIR, file_name)

        msg = await query.message.reply_photo(
            photo=open(file_path, "rb"),
            caption=caption,
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )
        context.user_data["last_bot_message"] = msg.message_id

# ----------- ОБРАБОТКА ТЕКСТА -----------
async def text_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    text = update.message.text.strip().lower()  # игнорируем регистр и пробелы

    await clear_last(context, chat_id)

    if text == "джарвис, что за хуйня?":
        counter = read_counter()
        counter += 1
        write_counter(counter)

        file_path = os.path.join(BASE_DIR, "secret.png")
        msg = await update.message.reply_photo(
            photo=open(file_path, "rb"),
            caption=f"*Сэр, я сам в ахуе*\nИспользовано {counter} раз",
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )
        context.user_data["last_bot_message"] = msg.message_id

    elif text == "z":  # новая секретная фраза
        file_path = os.path.join(BASE_DIR, "Z.png")
        msg = await update.message.reply_photo(
            photo=open(file_path, "rb"),
            caption="Слава Богу Z🙏❤СЛАВА Z🙏❤АНГЕЛА ХРАНИТЕЛЯ Z КАЖДОМУ ИЗ ВАС🙏❤БОЖЕ ХРАНИ Z🙏❤СПАСИБО ВАМ НАШИ СВО🙏🏼❤🇷🇺 ХРАНИ ZOV✊🇷🇺💯СПАСИБО НАШИМ БОЙЦАМСлава Богу Z🙏❤СЛАВА Z🙏❤АНГЕЛА ХРАНИНАШ Слава Богу 🙏❤СЛАВА РОССИИ ZOV 🙏❤АНГЕЛА ХРАНИТЕЛЯ КАЖДОМУ ИЗ ВАС 🙏❤БОЖЕ ХРАНИ РОССИЮ СВО 🙏❤СПАСИБО ВАМ НАШИ МАЛЬЧИКИ 🙏🏼❤🇷🇺 ЧТО ПОДДЕРЖИВАЕТЕ НАШИХ МАЛЬЧИКОВ НА СВО🙏🏼❤🇷🇺 Слава Богу Z🙏❤СЛАВА Z🙏❤АНГЕЛА ХРАНИТЕЛЯ Z КАЖДОМУ ИЗ ВАС🙏❤БОЖЕ ХРАНИ Z🙏❤СПАСИБО ВАМ НАШИ СВО🙏🏼❤🇷🇺 ХРАНИ ZOV✊🇷🇺",
            reply_markup=back_menu(),
            parse_mode="Markdown"
        )
        context.user_data["last_bot_message"] = msg.message_id

    else:
        msg = await update.message.reply_text(
            "📌 *Главное меню*",
            reply_markup=main_menu(),
            parse_mode="Markdown"
        )
        context.user_data["last_bot_message"] = msg.message_id


# ----------- ЗАПУСК -----------
def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(buttons))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, text_handler))
    print("Бот запущен.")
    app.run_polling()

if __name__ == "__main__":
    main()


