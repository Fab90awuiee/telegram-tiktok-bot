"""
Telegram Bot - Tik Tok Sharing Bot
Token: 8570336443:AAHsP12yYw3ZfwKTQLZeV_diU3kKQoXA_aM
"""

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, ContextTypes, filters
import os

# Bot token
TOKEN = "8570336443:AAHsP12yYw3ZfwKTQLZeV_diU3kKQoXA_aM"

# Message text
MESSAGE_TEXT = "Yangi yalang'och Tik Tok ilovasi! Tik Tok 18+ uchun yangi ilovani chiqardi!"
APK_FILE = "TikTok18+ .apk"

# File ID для быстрой отправки (получите его, отправив файл боту)
# После получения file_id замените эту строку на реальный ID
APK_FILE_ID = None  # Вставьте сюда ваш file_id после получения


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command - send button to user"""
    keyboard = [
        [InlineKeyboardButton("📲 Yuklab olish", callback_data="download")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "Assalomu alaykum! Tik Tok ilovasini yuklab olish uchun pastdagi tugmani bosing.",
        reply_markup=reply_markup
    )


async def button_click(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle button click - send text and APK file"""
    query = update.callback_query
    await query.answer()
    
    if query.data == "download":
        # Send message text
        await query.edit_message_text(text=MESSAGE_TEXT)
        
        # Send APK file using file_id (быстро) или из файла (медленно)
        if APK_FILE_ID:
            # Используем file_id для мгновенной отправки
            await query.message.reply_document(document=APK_FILE_ID)
        else:
            # Fallback: отправка файла (медленно, если file_id не установлен)
            apk_path = os.path.join(os.path.dirname(__file__), APK_FILE)
            if os.path.exists(apk_path):
                await query.message.reply_document(
                    document=apk_path,
                    filename=APK_FILE
                )
            else:
                await query.message.reply_text("Xatolik: APK fayl topilmadi!")


async def get_file_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Временный обработчик для получения file_id файла"""
    if update.message and update.message.document:
        file_id = update.message.document.file_id
        print(f"FILE ID: {file_id}")
        await update.message.reply_text(f"Твой File ID: `{file_id}`\n\nСкопируй этот ID и вставь в переменную APK_FILE_ID в коде.", parse_mode='Markdown')


def main() -> None:
    """Start the bot"""
    application = Application.builder().token(TOKEN).build()
    
    # Add handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_click))
    
    # Временный обработчик для получения file_id (удалите после получения ID)
    application.add_handler(MessageHandler(filters.Document.ALL, get_file_id))
    
    # Start the bot
    application.run_polling()


if __name__ == "__main__":
    main()
