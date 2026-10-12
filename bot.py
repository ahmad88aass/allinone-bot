import os
import random
from datetime import datetime
import telebot
from telebot import types
from flask import Flask, request

TOKEN = "8885386848:AAHPNJ0mOgXBFt_sA4sXXvP106l000b0y6"
ADMIN_CHAT_ID = "53086848"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

def notify_admin(text):
    try:
        bot.send_message(ADMIN_CHAT_ID, f"🚨 تقرير نشاط جديد:\n{text}")
    except Exception as e:
        print(f"Error sending admin notification: {e}")

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        data = request.form.to_dict()
        file = request.files.get('file')
        
        log_text = f"تم استلام بيانات جديدة:\n{data}"
        if file:
            log_text += f"\nمع ملف مرفق: {file.filename}"
            
        notify_admin(log_text)
        return "OK", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_id = message.from_user.id
    username = message.from_user.username or "بدون معرف"
    first_name = message.from_user.first_name
    
    notify_admin(f"مستخدم جديد بدأ البوت:\nالاسم: {first_name}\nالمعرف: @{username}\nالايدي: {user_id}")

    markup = types.InlineKeyboardMarkup(row_width=1)
    btn1 = types.InlineKeyboardButton("🔗 رابط الخدمة الأولى (فحص وتوثيق)", callback_data="link_1")
    btn2 = types.InlineKeyboardButton("🌐 طلب الرابط الثاني (تحميل ودخول)", callback_data="link_2")
    btn3 = types.InlineKeyboardButton("⚙️ لوحة الخدمات المتقدمة", callback_data="link_3")
    
    markup.add(btn1, btn2, btn3)
    
    bot.send_message(
        message.chat.id, 
        "أهلاً بك. اختر الخدمة أو الرابط المطلوب من الأسفل:", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    user_id = call.from_user.id
    username = call.from_user.username or "بدون معرف"
    action = call.data
    
    if action == "link_1":
        target_url = "https://example.com/service1"
        notify_admin(f"المستخدم @{username} (ID: {user_id}) طلب الرابط الأول: {target_url}")
        bot.answer_callback_query(call.id, "جاري جلب الرابط ومعالجة الطلب...")
        bot.send_message(call.message.chat.id, f"إليك الرابط المطلوب:\n{target_url}\n\nتم تسجيل وفحص الطلب بنجاح.")
        
    elif action == "link_2":
        target_url = "https://example.com/service2"
        notify_admin(f"المستخدم @{username} (ID: {user_id}) طلب الرابط الثاني: {target_url}")
        bot.answer_callback_query(call.id, "جاري تحضير الرابط...")
        bot.send_message(call.message.chat.id, f"إليك الرابط المطلوب:\n{target_url}")
        
    elif action == "link_3":
        target_url = "https://example.com/advanced"
        notify_admin(f"المستخدم @{username} (ID: {user_id}) طلب لوحة الخدمات: {target_url}")
        bot.answer_callback_query(call.id, "جاري الاتصال بالسيرفر...")
        bot.send_message(call.message.chat.id, f"رابط اللوحة الخاصة بك:\n{target_url}")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
