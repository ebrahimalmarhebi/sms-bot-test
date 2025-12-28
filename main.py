import os
from flask import Flask, request
import telebot

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "البوت شغال ✅")

@bot.message_handler(func=lambda m: True)
def echo(message):
    bot.reply_to(message, f"وصلت رسالتك: {message.text}")

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
