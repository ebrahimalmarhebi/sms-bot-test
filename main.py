import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# نجيب التوكن من Environment Variable
BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("✅ البوت شغال بنجاح")

def main():
    if not BOT_TOKEN:
        raise ValueError("❌ TELEGRAM_BOT_TOKEN غير موجود")

    app = Application.builder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))

    print("🤖 Bot is running...")
    app.run_polling()
