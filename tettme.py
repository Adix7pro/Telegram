import telebot
from telebot import types
from tmesql import sql_code
from datetime import date
import time
import datetime
from time import strftime
from telebot.types import InlineKeyboardButton, InlineKeyboardMarkup

ADMIN_ID = 5568951216  # Admin ID t.me dan olish kerak

bot = telebot.TeleBot("7260956364:AAG9Fz-CL2ftgjlcNdeJASAE-6jQK0bnCV8")  # Bot tokeningizni shu yerga joylashtiring

# # Asosiy tugmalar
# keyboard = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
# keyboard.row("Photo", "Video")
# keyboard.row("Audio", "Text")
# keyboard.row("Document")

# # Text ichidagi tugmalar
# keyboard1 = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
# keyboard1.row("Basic listening", "Developing listening")
# keyboard1.row("Expanding Listening", "Basic IELTS listening")
# keyboard1.row("Bosh Menu")
keyboard = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard.row("Photo 📷", "Video 🎥")
keyboard.row("Audio 🎧", "Text 📝")
keyboard.row("Document 📂")

keyboard1 = telebot.types.ReplyKeyboardMarkup(True, True)
keyboard1.row("Basic listening 📚", "Developing listening 📚")
keyboard1.row("Expanding Listening 📚", "Basic IELTS listening 📚")
keyboard1.row("Bosh Menu 🔙")

# Inline klaviatura
inline_keyboard = telebot.types.InlineKeyboardMarkup()
button_inline1 = telebot.types.InlineKeyboardButton(text="easy coding | main channel", url="https://t.me/+j9hrTs-9auhmMDhi")
button_inline2 = telebot.types.InlineKeyboardButton(text="world music", url="https://t.me/muzlifexd")
button_inline3 = telebot.types.InlineKeyboardButton(text="english sfera", url="https://t.me/bookshelvesx")

inline_keyboard.add(button_inline3, button_inline2)
inline_keyboard.add(button_inline1)

# STATISTIKA FUNCTION
@bot.message_handler(commands=["stat"])
def statistika(message):
    if message.from_user.id == ADMIN_ID:
        count = sql_code('''SELECT COUNT(*) FROM Users;''')
        if count:
            bot.send_message(ADMIN_ID, text=f"📊Bot statistikasi: {count[0][0]} ta")
        else:
            bot.send_message(ADMIN_ID, "📊Bot statistikasi: Ma'lumot topilmadi.")
    else:
        pass

# MAJBURIY A'ZO BO'LISH

def check_subscription(user_id):
    required_channels = ['@adix7pro', '@bookshelvesx']
    for channel_username in required_channels:
        try:
            member = bot.get_chat_member(channel_username, user_id)
            if member.status not in ['administrator', 'creator', 'member']:
                return False
        except Exception as e:
            print(f'Error checking membership for {channel_username}: {e}')
            return False
    return True

# Dekorator yaratish
def subscription_required(func):
    def wrapper(message, *args, **kwargs):
        user_id = message.from_user.id
        if check_subscription(user_id):
            return func(message, *args, **kwargs)
        else:
            markup = InlineKeyboardMarkup()
            markup.row(
                InlineKeyboardButton('Kanal1', url="https://t.me/adix7pro")
            )
            markup.row(
                InlineKeyboardButton('Kanal2', url="https://t.me/bookshelvesx")
            )
            markup.row(
                InlineKeyboardButton('Tekshirish', callback_data='check')
            )
            bot.send_message(message.chat.id, "Siz kanallarga obuna bo'lmagansiz. Iltimos, obuna bo'ling.", reply_markup=markup)
    return wrapper

# Start komandasi
@bot.message_handler(commands=["start"])
def startcom(message):
    user_id = message.from_user.id
    name = message.from_user.first_name

    # Foydalanuvchini ma'lumotlar bazasiga qo'shish
    sql_code(f'''INSERT INTO Users (user_id) VALUES ("{user_id}") ON DUPLICATE KEY UPDATE user_id=user_id;''')

    if check_subscription(user_id):
        bot.send_message(message.chat.id, f"📢 Xush kelibsiz, {name}! Siz obuna bo'lgansiz!", reply_markup=keyboard)
    else:
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton('Kanal1', url="https://t.me/adix7pro")
        )
        markup.row(
            InlineKeyboardButton('Kanal2', url="https://t.me/bookshelvesx")
        )
        markup.row(
            InlineKeyboardButton('Tekshirish', callback_data='check')
        )
        bot.send_message(message.chat.id, "📢 Siz kanallarga obuna bo'lmagansiz. Iltimos, obuna bo'ling.", reply_markup=markup)

# Tekshirish uchun callback
@bot.callback_query_handler(func=lambda call: call.data == 'check')
def check_subscription_callback(call):
    user_id = call.from_user.id
    name = call.from_user.first_name  # Foydalanuvchi nomini olish

    if check_subscription(user_id):
        bot.send_message(call.message.chat.id, f"✅ {name}, siz kanallarga obuna bo'lgansiz!", reply_markup=keyboard)
    else:
        markup = InlineKeyboardMarkup()
        markup.row(
            InlineKeyboardButton('Kanal1', url="https://t.me/adix7pro")
        )
        markup.row(
            InlineKeyboardButton('Kanal2', url="https://t.me/bookshelvesx")
        )
        markup.row(
            InlineKeyboardButton('Tekshirish', callback_data='check')
        )
        bot.send_message(call.message.chat.id, "❌ Siz hanuz kanallarga obuna bo'lmagansiz. Iltimos, obuna bo'ling.", reply_markup=markup)

# Xabar yuborish komandasi
@bot.message_handler(commands=["xabar"])
def send_to_all_users(message):
    if message.from_user.id == ADMIN_ID:
        try:
            bot.send_message(ADMIN_ID, "Yuborilayotgan Xabarni kiriting:")
            bot.register_next_step_handler(message, forward_content_to_all)
        except Exception:
            bot.send_message(ADMIN_ID, "Xatolik bo'ldi❌")
    else:
        pass

def forward_content_to_all(message):
    try:
        content_type = message.content_type
        if content_type == "text":
            user_message = message.text
            users = sql_code('''SELECT user_id FROM Users''')
            for x in users:
                user_id = x[0]
                try:
                    bot.send_message(user_id, f"{user_message}")
                except Exception:
                    bot.send_message(ADMIN_ID, f"Xatolik: Foydalanuvchi {user_id} ga yuborilmadi.")
            bot.send_message(ADMIN_ID, text="✅ Xabar muvaffaqiyatli yuborildi!")
        else:
            bot.send_message(ADMIN_ID, "Foydalanuvchilarga faqat matnli xabar yuborish mumkin.")
    except Exception:
        bot.send_message(ADMIN_ID, "Xatolik bo'ldi❌")

# Foydalanuvchilarning asosiy tugma handleri
@bot.message_handler(func=lambda message: True)
@subscription_required
def xabar(message):
    if message.text == "Photo 📷":
        bot.send_photo(message.chat.id, "https://t.me/adix7pro/78", caption="Ushbu bot AdiXpro tomonidan yaratildi")
    elif message.text == "Video 🎥":
        bot.send_video(message.chat.id, "https://t.me/adix7pro/92", caption="Ushbu bot AdiXpro tomonidan yaratildi")
    elif message.text == "Audio 🎧":
        bot.send_audio(message.chat.id, "https://t.me/muzlifexd/206", caption="Ushbu bot AdiXpro tomonidan yaratildi")
    elif message.text == "Text 📝":
        bot.send_message(message.chat.id, "Assalom alaykum bot admini : @Adham_AI", reply_markup=inline_keyboard)  # Textga caption qo'shib bo'lmadi
    elif message.text == "Document 📂":
        bot.send_document(message.chat.id, "https://t.me/adix7pro/100", caption="Ushbu bot AdiXpro tomonidan yaratildi", reply_markup=keyboard1)
    elif message.text == "Basic listening 📚":
        bot.send_document(message.chat.id, "https://t.me/bookshelvesx/308", caption="Ushbu bot AdiXpro tomonidan yaratildi")
    elif message.text == "Developing listening 📚":
        bot.send_document(message.chat.id, "https://t.me/bookshelvesx/630", caption="Ushbu bot AdiXpro tomonidan yaratildi")
    elif message.text == "Expanding Listening 📚":
        bot.send_document(message.chat.id, "https://t.me/bookshelvesx/184", caption="Ushbu bot AdiXpro tomonidan yaratildi")
    elif message.text == "Basic IELTS listening 📚":
        bot.send_document(message.chat.id, "https://t.me/bookshelvesx/82", caption="Ushbu bot AdiXpro tomonidan yaratildi")  # Textga caption qo'shib bo'lmadi
    elif message.text == "Bosh Menu 🔙":
        bot.send_message(message.chat.id, "Orqaga qaytdingiz", reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "Noma'lum buyruq. Iltimos, quyidagi tugmalardan birini tanlang.", reply_markup=keyboard)

# Inline tugmalar uchun handler
# @bot.callback_query_handler(func=lambda call: True)
# def inlinedef(call):
#     if call.data == "tugma2":
#         bot.send_video(call.message.chat.id, "https://t.me/adix7pro/101", caption="Bu Video")
#         bot.answer_callback_query(call.id, "Video yuborildi", cache_time=0)
#     elif call.data == "tugma3":
#         bot.send_photo(call.message.chat.id, "https://t.me/adix7pro/102", caption='Bu rasm')
#         bot.answer_callback_query(call.id, "Rasm yuborildi", cache_time=0)
#     else:
#         bot.answer_callback_query(call.id, "Noma'lum tugma", cache_time=0)

bot.polling()