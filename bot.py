import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    await update.message.reply_text('Hi! Send me any text, and I will count the words and characters for you.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when /help is issued."""
    await update.message.reply_text('Just send me a text message, and I will reply with the word and character count.')

async def count_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count words and characters in the received text message."""
    text = update.message.text
    word_count = len(text.split())
    char_count = len(text)
    response = f"📝 Word count: {word_count}\n🔠 Character count: {char_count}"
    await update.message.reply_text(response)

if __name__ == '__main__':
    if not BOT_TOKEN:
        logging.error("BOT_TOKEN environment variable not set!")
        exit(1)
    
    # Create the Application
    application = ApplicationBuilder().token(BOT_TOKEN).build()
    
    # Register command handlers
    application.add_handler(CommandHandler('start', start))
    application.add_handler(CommandHandler('help', help_command))
    
    # Register a handler for all text messages
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_words))
    
    # Start the bot with long polling
    logging.info("Starting bot with long polling...")
    application.run_polling()
