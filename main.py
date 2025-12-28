import os
from flask import Flask, request
import telebot
from telebot import types

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

app = Flask(__name__)

# تخزين حالة المستخدم مؤقتًا
user_state = {}

# ---------- واجهات الأزرار ----------

def main_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("📱 شراء رقم", callback_data="buy"),
        types.InlineKeyboardButton("📊 الحالة الحالية", callback_data="status"),
    )
    kb.add(
        types.InlineKeyboardButton("❌ إلغاء", callback_data="cancel")
    )
    return kb

def service_menu():
    kb = types.InlineKeyboardMarkup(row_width=2)
    kb.add(
        types.InlineKeyboardButton("🟦 Telegram", callback_data="service_telegram"),
        types.InlineKeyboardButton("🟩 WhatsApp", callback_data="service_whatsapp"),
    )
    kb.add(
        types.InlineKeyboardButton("🟨 Google", callback_data="service_google"),
        types.InlineKeyboardButton("🟥 Facebook", callback_data="service_facebook"),
    )
    kb.add(
        types.InlineKeyboardButton("🔙 رجوع", callback_data="back_main")
    )
    return kb

# ---------- أوامر ----------

@bot.message_handler(commands=['start'])
def start(message):
    user_state[message.chat.id] = {}
    bot.send_message(
        message.chat.id,
        "مرحباً 👋\nاختر الخدمة من القائمة:",
        reply_markup=main_menu()
    )

# ---------- معالجة الأزرار ----------

@bot.callback_query_handler(func=lambda call: True)
def callbacks(call):
    chat_id = call.message.chat.id

    if call.data == "buy":
        user_state[chat_id] = {"step": "service"}
        bot.edit_message_text(
            "اختر الخدمة:",
            chat_id,
            call.message.message_id,
            reply_markup=service_menu()
        )

    elif call.data.startswith("service_"):
        service = call.data.replace("service_", "")
        user_state[chat_id]["service"] = service
        user_state[chat_id]["step"] = "country"

        bot.edit_message_text(
            f"اخترت الخدمة: {service.capitalize()}\n\n"
            "✍️ اكتب اسم الدولة أو رمزها:\n"
            "مثال: +966 أو Saudi",
            chat_id,
            call.message.message_id
        )

    elif call.data == "status":
        state = user_state.get(chat_id)
        if not state:
            text = "لا توجد عملية حالية."
        else:
            text = (
                "📊 الحالة الحالية:\n"
                f"الخدمة: {state.get('service', '-')}\n"
                f"الدولة: {state.get('country', '-')}\n"
                f"الحالة: {state.get('step', '-')}"
            )

        bot.answer_callback_query(call.id)
        bot.send_message(chat_id, text)

    elif call.data == "cancel":
        user_state.pop(chat_id, None)
        bot.edit_message_text(
            "❌ تم إلغاء العملية.",
            chat_id,
            call.message.message_id,
            reply_markup=main_menu()
        )

    elif call.data == "back_main":
        bot.edit_message_text(
            "مرحباً 👋\nاختر الخدمة من القائمة:",
            chat_id,
            call.message.message_id,
            reply_markup=main_menu()
        )

# ---------- إدخال الدولة ----------

@bot.message_handler(func=lambda m: user_state.get(m.chat.id, {}).get("step") == "country")
def get_country(message):
    state = user_state.get(message.chat.id)
    state["country"] = message.text
    state["step"] = "waiting"

    bot.send_message(
        message.chat.id,
        f"📞 تم اختيار الخدمة:\n{state['service'].capitalize()}\n"
        f"🌍 الدولة: {state['country']}\n\n"
        f"⏳ بانتظار كود التفعيل..."
    )

# ---------- Webhook ----------

@app.route("/telegram", methods=["POST"])
def telegram_webhook():
    update = telebot.types.Update.de_json(
        request.stream.read().decode("utf-8")
    )
    bot.process_new_updates([update])
    return "OK", 200

@app.route("/")
def index():
    return "OK"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
