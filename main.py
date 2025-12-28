import os
from telegram.ext import Updater, CommandHandler

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")

def start(update, context):
    update.message.reply_text("✅ البوت شغال تمام")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher

    dp.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
