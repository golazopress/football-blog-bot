import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from blogbot import run_blog_bot
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def generate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("⚡ Generating blog...")
    run_blog_bot()
    await update.message.reply_text("✅ Blog sent!")

def main():
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
    app.add_handler(CommandHandler("generate", generate))
    app.run_polling()

if __name__ == "__main__":
    main()
