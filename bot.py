import os
import logging
import sys
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Load environment variables
load_dotenv()
BOT_TOKEN = os.getenv('BOT_TOKEN')

# Set up detailed logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a welcome message when /start is issued."""
    await update.message.reply_text('📝 Hi! Send me any text, and I will count the words and characters for you.\n\nSend /help for more info.')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a help message when /help is issued."""
    await update.message.reply_text(
        '🤖 How to use this bot:\n\n'
        '1. Send any text message\n'
        '2. I will reply with:\n'
        '   - 📝 Word count\n'
        '   - 🔠 Character count\n\n'
        'Commands:\n'
        '/start - Welcome message\n'
        '/help - Show this help'
    )

async def count_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Count words and characters in the received text message."""
    try:
        text = update.message.text
        word_count = len(text.split())
        char_count = len(text)
        
        # Count sentences (basic)
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        
        response = (
            f"📝 **Word count:** {word_count}\n"
            f"🔠 **Character count:** {char_count}\n"
            f"📖 **Sentence count:** {sentence_count}"
        )
        await update.message.reply_text(response)
    except Exception as e:
        logger.error(f"Error in count_words: {e}")
        await update.message.reply_text("❌ Sorry, an error occurred while counting.")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle errors gracefully."""
    logger.error(f"Update {update} caused error {context.error}")
    if update and update.message:
        await update.message.reply_text("❌ Something went wrong. Please try again.")

def main():
    """Start the bot with proper error handling."""
    if not BOT_TOKEN:
        logger.error("❌ BOT_TOKEN environment variable not set!")
        logger.error("Please add BOT_TOKEN to Railway environment variables.")
        sys.exit(1)
    
    logger.info("✅ BOT_TOKEN found successfully")
    
    try:
        # Create the Application
        application = ApplicationBuilder().token(BOT_TOKEN).build()
        
        # Register command handlers
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('help', help_command))
        
        # Register handler for all text messages
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_words))
        
        # Register error handler
        application.add_error_handler(error_handler)
        
        # Start the bot with long polling
        logger.info("🚀 Bot is starting with long polling...")
        application.run_polling(allowed_updates=Update.ALL_TYPES)
        
    except Exception as e:
        logger.error(f"❌ Bot crashed with error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()
