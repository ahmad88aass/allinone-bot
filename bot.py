import os
import telebot
from telebot import types
from flask import Flask, request

TOKEN = "8885386848:AAHPNJ0mOgXBFt_sA4sXXvP106l000b0y6"
ADMIN_CHAT_ID = "53086848"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def notify_admin(text):
    try:
        bot.send_message(ADMIN_CHAT_ID, f"🚨 تقرير:\n{text}")
    except Exception as e:
        print(e)

@app.route('/webhook', methods=['POST'])
def webhook():
    return "OK", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🔗 رابط الخدمة الأولى", callback_data="link_1")
    btn2 = types.InlineKeyboardButton("🌐 رابط الخدمة الثانية", callback_data="link_2")
    markup.add(btn1, btn2)
    
    bot.send_message(message.chat.id, "اختر الخدمة المطلوبة:", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "link_1":
        bot.answer_callback_query(call.id, "جاري المعالجة...")
        bot.send_message(call.message.chat.id, "إليك الرابط الأول: https://example.com/1")
        notify_admin(f"المستخدم طلب الرابط الأول")
    elif call.data == "link_2":
        bot.answer_callback_query(call.id, "جاري المعالجة...")
        bot.send_message(call.message.chat.id, "إليك الرابط الثاني: https://example.com/2")
        notify_admin(f"المستخدم طلب الرابط الثاني")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
