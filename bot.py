import os
import sys
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Force flush stdout/stderr immediately
sys.stdout.reconfigure(line_buffering=True)
sys.stderr.reconfigure(line_buffering=True)

# Set up logging to see everything
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.DEBUG,  # DEBUG level gives maximum info
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

logger.info("🚀 BOT STARTING UP...")
logger.info(f"🔍 Python version: {sys.version}")

# Try loading environment variables
logger.info("📂 Loading environment variables...")
load_dotenv()

# Get token - try multiple methods
BOT_TOKEN = os.getenv('BOT_TOKEN')
if not BOT_TOKEN:
    # Try alternative method
    BOT_TOKEN = os.environ.get('BOT_TOKEN')
    
if not BOT_TOKEN:
    logger.error("❌❌❌ CRITICAL: BOT_TOKEN environment variable not found!")
    logger.error("💡 Please add BOT_TOKEN to Railway environment variables")
    logger.error("💡 Check: Railway Dashboard → Variables → Add BOT_TOKEN")
    sys.exit(1)

logger.info(f"✅ BOT_TOKEN found! Length: {len(BOT_TOKEN)} characters")
logger.info(f"✅ Token starts with: {BOT_TOKEN[:10]}...")

# Handler functions
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📩 /start command received from {update.effective_user.username}")
    await update.message.reply_text(
        '📝 **Word Counter Bot**\n\n'
        'Send me any text and I\'ll count:\n'
        '• Words 📝\n'
        '• Characters 🔠\n'
        '• Sentences 📖\n\n'
        'Send /help for commands'
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.info(f"📩 /help command received from {update.effective_user.username}")
    await update.message.reply_text(
        '🤖 **Commands:**\n'
        '/start - Welcome message\n'
        '/help - Show this help\n\n'
        '📝 **Just send any text!**'
    )

async def count_words(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        text = update.message.text
        logger.info(f"📩 Counting text from {update.effective_user.username}: {len(text)} chars")
        
        word_count = len(text.split())
        char_count = len(text)
        sentence_count = text.count('.') + text.count('!') + text.count('?')
        
        response = (
            f"📝 **Word count:** {word_count}\n"
            f"🔠 **Character count:** {char_count}\n"
            f"📖 **Sentence count:** {sentence_count}"
        )
        await update.message.reply_text(response)
        logger.info(f"✅ Response sent: {word_count} words, {char_count} chars")
    except Exception as e:
        logger.error(f"❌ Error in count_words: {e}", exc_info=True)
        await update.message.reply_text("❌ Sorry, something went wrong!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"❌ Update {update} caused error: {context.error}", exc_info=True)

# Main function
def main():
    logger.info("🏗️ Building bot application...")
    
    try:
        # Build application with timeout settings
        application = ApplicationBuilder() \
            .token(BOT_TOKEN) \
            .connect_timeout(30.0) \
            .read_timeout(30.0) \
            .build()
        
        logger.info("✅ Application built successfully")
        
        # Add handlers
        application.add_handler(CommandHandler('start', start))
        application.add_handler(CommandHandler('help', help_command))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, count_words))
        application.add_error_handler(error_handler)
        
        logger.info("✅ Handlers registered")
        logger.info("🚀 STARTING BOT WITH POLLING...")
        
        # Start polling with error handling
        application.run_polling(
            allowed_updates=Update.ALL_TYPES,
            drop_pending_updates=True
        )
        
    except Exception as e:
        logger.error(f"❌❌❌ FATAL ERROR: {e}", exc_info=True)
        sys.exit(1)

if __name__ == '__main__':
    main()
