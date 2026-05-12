import telebot
from telebot import types
import re
import traceback
from collections import defaultdict

TOKEN = "8514273761:AAH3YeenOrWomYPUZve9NadLfwLB1py9P18"

ADMIN_ID = 8504692404

REVIEWS_LINK = "https://t.me/SanyaRysel"

SUPPORT_USERNAME = "@veryselov"

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# ================= DATA =================

user_data = defaultdict(dict)

user_step = {}

orders = {} order_id = 1

# ================= VALIDATION =================

def is_valid_gmail(email):

pattern = r'^[a-zA-Z0-9._%+-]+@gmail\.com$'

return re.match(pattern, email, re.IGNORECASE)

# ================= PRICE =================

def calculate_price(subs, region, platform):

subs = int(subs)

# ================= YOUTUBE PRICE =================

if platform == "YouTube":

    stars = 0

    if 1 <= subs <= 10:
        price = 25

    elif 10 < subs <= 50:
        price = 30

    elif 50 < subs <= 100:
        price = 40
        stars = 15

    elif 100 < subs <= 200:
        price = 50
        stars = 25

    elif 200 < subs <= 350:
        price = 75
        stars = 25

    elif 350 < subs <= 500:
        price = 90
        stars = 50

    elif 500 < subs <= 650:
        price = 120
        stars = 65

    elif 650 < subs <= 750:
        price = 140
        stars = 65

    elif 750 < subs <= 1000:
        price = 200
        stars = 75

    elif 1000 < subs <= 1500:
        price = 300
        stars = 125

    elif 1500 < subs <= 2000:
        price = 450
        stars = 175

    elif 2000 < subs <= 3000:
        price = 750
        stars = 250

    elif 3000 < subs <= 5000:
        price = 900
        stars = 500

    elif 5000 < subs <= 10000:
        price = 1500
        stars = 1000

    elif 10000 < subs <= 20000:
        price = 2000
        stars = 1450

    elif 20000 < subs <= 35000:
        price = 3000
        stars = 1750

    elif 35000 < subs <= 50000:
        price = 5000
        stars = 2000

    else:
        price = 5000
        stars = 2500

    if region == "🇺🇸 USA":
        price = int(price * 1.10)

    elif region == "🇷🇺 Russia":
        price = int(price * 0.90)

    return f"{price} сом / {stars} ⭐"

# ================= TIKTOK PRICE =================

elif platform == "TikTok":

    if subs < 500:
        return "❌ Для TikTok минимум 500 подписчиков"

    elif 500 <= subs <= 750:
        return "100 сом / 50 ⭐"

    elif 750 < subs <= 1000:
        return "200 сом / 100 ⭐"

    elif 1000 < subs <= 1250:
        return "250 сом / 125 ⭐"

    elif 1250 < subs <= 1500:
        return "300 сом / 150 ⭐"

    elif 1500 < subs <= 1750:
        return "500 сом / 250 ⭐"

    elif 1750 < subs <= 2000:
        return "700 сом / 350 ⭐"

    elif 2000 < subs <= 2500:
        return "900 сом / 500 ⭐"

    elif 2500 < subs <= 3000:
        return "1250 сом / 750 ⭐"

    elif 3000 < subs <= 3500:
        return "1799 сом / 999 ⭐"

    elif 3500 < subs <= 4000:
        return "2000 сом / 1150 ⭐"

    elif 4000 < subs <= 5000:
        return "2500 сом / 1250 ⭐"

    else:
        return "📞 Договорная\nНапишите поддержке для торговли аккаунта"

# ================= KEYBOARDS =================

def main_menu_markup():

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

markup.row(types.KeyboardButton("💸 Продать канал"))

markup.row(
    types.KeyboardButton("⭐ Отзывы"),
    types.KeyboardButton("🛠 Поддержка")
)

markup.row(types.KeyboardButton("📦 Статус заказа"))

return markup

def back_markup():

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

markup.row(
    types.KeyboardButton("⬅️ Назад"),
    types.KeyboardButton("🏠 Меню")
)

return markup

# ================= MAIN MENU =================

def send_main_menu(chat_id):

user_step.pop(chat_id, None)

text = """

🔥 <b>RySell Shop</b>

💎 Скупка YouTube/TikTok каналов ⚡ Быстрые выплаты 🛡 Поддержка 24/7

👇 Выберите действие ниже """

bot.send_message(
    chat_id,
    text,
    reply_markup=main_menu_markup()
)

# ================= START =================

@bot.message_handler(commands=['start']) def start(message):

send_main_menu(message.chat.id)

# ================= MENU =================

@bot.message_handler(func=lambda m: m.text == "🏠 Меню") def menu_handler(message):

send_main_menu(message.chat.id)

# ================= REVIEWS =================

@bot.message_handler(func=lambda m: m.text == "⭐ Отзывы") def reviews_handler(message):

bot.send_message(
    message.chat.id,
    f"⭐ Отзывы:\n\n{REVIEWS_LINK}"
)

# ================= SUPPORT =================

@bot.message_handler(func=lambda m: m.text == "🛠 Поддержка") def support_handler(message):

bot.send_message(
    message.chat.id,
    f"🛠 Поддержка:\n\n{SUPPORT_USERNAME}"
)

# ================= STATUS =================

@bot.message_handler(func=lambda m: m.text == "📦 Статус заказа") def status_handler(message):

chat_id = message.chat.id

result = []

for num, data in orders.items():

    if data["user_id"] == chat_id:

        result.append(
            f"📦 Заказ #{num}\n📌 Статус: {data['status']}"
        )

if not result:

    bot.send_message(
        chat_id,
        "❌ У вас нет заказов"
    )

    return

bot.send_message(
    chat_id,
    "\n\n".join(result)
)

# ================= SELL =================

@bot.message_handler(func=lambda m: m.text == "💸 Продать канал") def sell_handler(message):

chat_id = message.chat.id

user_data[chat_id] = {}

ask_platform(chat_id)

def ask_platform(chat_id):

user_step[chat_id] = "platform"

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

markup.row(
    types.KeyboardButton("🎬 YouTube"),
    types.KeyboardButton("🎵 TikTok")
)

markup.row(
    types.KeyboardButton("⬅️ Назад"),
    types.KeyboardButton("🏠 Меню")
)

bot.send_message(
    chat_id,
    "🎬 Выберите платформу:",
    reply_markup=markup
)

# ================= ASK FUNCTIONS =================

def ask_region(chat_id):

user_step[chat_id] = "region"

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

markup.row(
    types.KeyboardButton("🇺🇸 USA"),
    types.KeyboardButton("🇷🇺 Russia")
)

markup.row(types.KeyboardButton("🌍 Другое"))

markup.row(
    types.KeyboardButton("⬅️ Назад"),
    types.KeyboardButton("🏠 Меню")
)

bot.send_message(
    chat_id,
    "🌍 Укажите регион канала",
    reply_markup=markup
)

def ask_subs(chat_id):

user_step[chat_id] = "subs"

bot.send_message(
    chat_id,
    "👥 Сколько подписчиков?",
    reply_markup=back_markup()
)

def ask_content(chat_id):

user_step[chat_id] = "content"

bot.send_message(
    chat_id,
    "🎬 Какая тематика канала?",
    reply_markup=back_markup()
)

def ask_agreement(chat_id):

user_step[chat_id] = "agreement"

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

markup.row(
    types.KeyboardButton("✅ Согласиться"),
    types.KeyboardButton("❌ Отказаться")
)

markup.row(
    types.KeyboardButton("⬅️ Назад"),
    types.KeyboardButton("🏠 Меню")
)

price = user_data[chat_id]["price"]

bot.send_message(
    chat_id,
    f"💰 Ваш аккаунт предварительно оценен в {price}\n\nПродать аккаунт?",
    reply_markup=markup
)

def ask_gmail(chat_id):

user_step[chat_id] = "gmail"

bot.send_message(
    chat_id,
    "📧 Отправьте Gmail",
    reply_markup=back_markup()
)

def ask_password(chat_id):

user_step[chat_id] = "password"

bot.send_message(
    chat_id,
    "🔑 Отправьте пароль",
    reply_markup=back_markup()
)

def ask_bank(chat_id):

user_step[chat_id] = "bank"

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

markup.row(
    types.KeyboardButton("⭐ Telegram Stars"),
    types.KeyboardButton("💳 VISA")
)

markup.row(
    types.KeyboardButton("🟢 Mbank"),
    types.KeyboardButton("🔵 Bakai")
)

markup.row(types.KeyboardButton("🟡 O! Деньги"))

markup.row(
    types.KeyboardButton("⬅️ Назад"),
    types.KeyboardButton("🏠 Меню")
)

bot.send_message(
    chat_id,
    "💸 Выберите способ выплаты",
    reply_markup=markup
)

def ask_method(chat_id):

bank = user_data[chat_id]["bank"]

if bank == "⭐ Telegram Stars":

    user_step[chat_id] = "stars"

    bot.send_message(
        chat_id,
        "⭐ Отправьте Telegram username",
        reply_markup=back_markup()
    )

    return

if bank == "💳 VISA":

    user_step[chat_id] = "visa"

    bot.send_message(
        chat_id,
        "💳 Отправьте номер карты",
        reply_markup=back_markup()
    )

    return

user_step[chat_id] = "method"

markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

markup.row(
    types.KeyboardButton("📱 Номер телефона"),
    types.KeyboardButton("💳 Номер карты")
)

markup.row(types.KeyboardButton("📷 QR-код"))

markup.row(
    types.KeyboardButton("⬅️ Назад"),
    types.KeyboardButton("🏠 Меню")
)

bot.send_message(
    chat_id,
    "💳 Выберите способ получения",
    reply_markup=markup
)

def ask_payment(chat_id):

user_step[chat_id] = "payment"

method = user_data[chat_id]["method"]

if method == "📱 Номер телефона":

    bot.send_message(
        chat_id,
        "📱 Отправьте номер телефона",
        reply_markup=back_markup()
    )

elif method == "💳 Номер карты":

    bot.send_message(
        chat_id,
        "💳 Отправьте номер карты",
        reply_markup=back_markup()
    )

elif method == "📷 QR-код":

    bot.send_message(
        chat_id,
        "📷 Отправьте QR-код фото",
        reply_markup=back_markup()
    )

# ================= CREATE ORDER =================

def create_order(chat_id, payment_data):

global order_id

data = user_data[chat_id]

orders[order_id] = {
    "user_id": chat_id,
    "status": "⏳ На проверке"
}

admin_text = f"""

📦 <b>Новая заявка #{order_id}</b>

🎬 Платформа: {data['platform']} 🌍 Регион: {data['region']} 👥 Подписчики: {data['subs']} 🎬 Тематика: {data['content']}

💰 Цена: {data['price']}

📧 Gmail: {data['gmail']} 🔑 Пароль: {data['password']}

🏦 Выплата: {data['bank']} 💸 Метод: {data['method']}

📌 Реквизиты: {payment_data}

👤 USER ID: {chat_id} """

markup = types.InlineKeyboardMarkup()

markup.row(
    types.InlineKeyboardButton(
        "✅ Оплачено",
        callback_data=f"paid_{order_id}_{chat_id}"
    ),
    types.InlineKeyboardButton(
        "❌ Отказать",
        callback_data=f"reject_{order_id}_{chat_id}"
    )
)

if data.get("qr_photo"):

    bot.send_photo(
        ADMIN_ID,
        data["qr_photo"],
        caption=admin_text,
        reply_markup=markup
    )

else:

    bot.send_message(
        ADMIN_ID,
        admin_text,
        reply_markup=markup
    )

bot.send_message(
    chat_id,
    f"✅ Ваша заявка #{order_id} отправлена",
    reply_markup=main_menu_markup()
)

order_id += 1

user_step.pop(chat_id, None)
user_data.pop(chat_id, None)

# ================= BACK =================

def handle_back(chat_id):

step = user_step.get(chat_id)

if step == "platform":
    send_main_menu(chat_id)

elif step == "region":
    ask_platform(chat_id)

elif step == "subs":
    ask_region(chat_id)

elif step == "content":
    ask_subs(chat_id)

elif step == "agreement":
    ask_content(chat_id)

elif step == "gmail":
    ask_agreement(chat_id)

elif step == "password":
    ask_gmail(chat_id)

elif step == "bank":
    ask_password(chat_id)

elif step == "method":
    ask_bank(chat_id)

elif step == "payment":
    ask_method(chat_id)

elif step == "stars":
    ask_bank(chat_id)

elif step == "visa":
    ask_bank(chat_id)

# ================= CALLBACK =================

@bot.callback_query_handler(func=lambda call: True) def callback_handler(call):

try:

    if call.from_user.id != ADMIN_ID:
        return

    data = call.data

    if data.startswith("paid_"):

        _, order_num, user_id = data.split("_")

        order_num = int(order_num)
        user_id = int(user_id)

        orders[order_num]["status"] = "✅ Оплачено"

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )

        bot.send_message(
            user_id,
            f"✅ Заказ #{order_num} оплачен"
        )

    elif data.startswith("reject_"):

        _, order_num, user_id = data.split("_")

        order_num = int(order_num)
        user_id = int(user_id)

        orders[order_num]["status"] = "❌ Отказано"

        bot.edit_message_reply_markup(
            call.message.chat.id,
            call.message.message_id,
            reply_markup=None
        )

        bot.send_message(
            user_id,
            f"❌ Заказ #{order_num} отклонен"
        )

except Exception as e:
    print(e)

# ================= MAIN =================

@bot.message_handler(content_types=['text', 'photo']) def all_messages(message):

try:

    chat_id = message.chat.id
    text = message.text if message.content_type == "text" else ""

    if text == "⬅️ Назад":
        handle_back(chat_id)
        return

    if chat_id not in user_step:
        return

    step = user_step[chat_id]

    # PLATFORM
    if step == "platform":

        if text == "🎬 YouTube":
            user_data[chat_id]["platform"] = "YouTube"

        elif text == "🎵 TikTok":
            user_data[chat_id]["platform"] = "TikTok"

        else:

            bot.send_message(
                chat_id,
                "❌ Выберите платформу кнопками"
            )

            return

        ask_region(chat_id)

    # REGION
    elif step == "region":

        user_data[chat_id]["region"] = text

        ask_subs(chat_id)

    # SUBS
    elif step == "subs":

        if not text.isdigit():

            bot.send_message(
                chat_id,
                "❌ Введите только цифры"
            )

            return

        subs = int(text)

        platform = user_data[chat_id]["platform"]

        if platform == "TikTok" and subs < 500:

            bot.send_message(
                chat_id,
                "❌ Для TikTok минимум 500 подписчиков"
            )

            return

        user_data[chat_id]["subs"] = subs

        region = user_data[chat_id]["region"]

        user_data[chat_id]["price"] = calculate_price(
            subs,
            region,
            platform
        )

        ask_content(chat_id)

    # CONTENT
    elif step == "content":

        user_data[chat_id]["content"] = text

        ask_agreement(chat_id)

    # AGREEMENT
    elif step == "agreement":

        if text == "❌ Отказаться":

            bot.send_message(
                chat_id,
                "❌ Продажа отменена",
                reply_markup=main_menu_markup()
            )

            user_step.pop(chat_id, None)
            user_data.pop(chat_id, None)

            return

        if text == "✅ Согласиться":

            ask_gmail(chat_id)

            return

    # GMAIL
    elif step == "gmail":

        if not is_valid_gmail(text):

            bot.send_message(
                chat_id,
                "❌ Отправьте корректный Gmail"
            )

            return

        user_data[chat_id]["gmail"] = text

        ask_password(chat_id)

    # PASSWORD
    elif step == "password":

        user_data[chat_id]["password"] = text

        ask_bank(chat_id)

    # BANK
    elif step == "bank":

        user_data[chat_id]["bank"] = text

        ask_method(chat_id)

    # METHOD
    elif step == "method":

        user_data[chat_id]["method"] = text

        ask_payment(chat_id)

    # STARS
    elif step == "stars":

        user_data[chat_id]["bank"] = "⭐ Telegram Stars"
        user_data[chat_id]["method"] = "⭐ Username"

        create_order(chat_id, text)

    # VISA
    elif step == "visa":
н
        user_data[chat_id]["bank"] = "💳 VISA"
        user_data[chat_id]["method"] = "💳 Карта"

        create_order(chat_id, text)

    # PAYMENT
    elif step == "payment":

        if message.content_type == "photo":

            user_data[chat_id]["qr_photo"] = message.photo[-1].file_id

            create_order(chat_id, "📷 QR-код")

            return

        create_order(chat_id, text)

except Exception as e:

    print("ERROR:", e)
    traceback.print_exc()

    bot.send_message(
        message.chat.id,
        "❌ Произошла ошибка"
    )

    send_main_menu(message.chat.id)

# ================= RUN =================

print("Бот запущен")

while True:

try:

    bot.infinity_polling(
        timeout=30,
        long_polling_timeout=30,
        skip_pending=True
    )

except Exception as e:

    print("Polling Error:", e)
