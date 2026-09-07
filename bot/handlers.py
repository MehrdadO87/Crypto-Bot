from telebot import *
from api import get_price
import core.query
from core.membership import is_user_member, join_channel_markup

def get_main_keyboard(user_id):
    phone_number = core.query.get_user_phone(user_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    prices_button = types.KeyboardButton("💰 Check Prices")
    support_button = types.KeyboardButton("💬 Contact Support")
    if phone_number:
        account_button = types.KeyboardButton("👤 My Account")
        keyboard.row(account_button,prices_button)
    else:
        register_button = types.KeyboardButton("📝 Register")
        keyboard.row(register_button,prices_button)
    keyboard.row(support_button)
    return keyboard

def mask_phone(phone_number):
    if not phone_number:
        return "Not set"

    if len(phone_number) <= 7:
        return "*" * len(phone_number)

    return phone_number[:3] + "*" * (len(phone_number) - 6) + phone_number[-3:]

def register_handlers(bot: TeleBot):
    @bot.message_handler(commands=['start'])
    def start_handler(message):
        if not is_user_member(bot, message.from_user.id):
            bot.send_message(
                message.chat.id,
                "🔒 To use Crypto Mehrdad, please join our channel first.",
                reply_markup=join_channel_markup()
            )
            return
        user_id = message.from_user.id
        user_name = message.from_user.username
        user_fname = message.from_user.first_name
        user_lname = message.from_user.last_name
        markup = get_main_keyboard(user_id)
        bot.send_message(message.chat.id, """Welcome to Crypto Mehrdad!👋

    📈 Get the latest cryptocurrency prices quickly and easily.

    - Check the top 5 cryptocurrencies
    - View real-time prices
    - Simple and fast

    Use the buttons below to get started.""", reply_markup=markup)


    @bot.message_handler(func=lambda message: message.text == "💬 Contact Support")
    def sopport_handler(message):
        bot.send_message(message.chat.id, "If you have any questions, problems or suggestions, feel free to contact our support team.\n\n💬 Support: @Mehrdaddg69\n\nWe'll be happy to help!")

    @bot.message_handler(func=lambda message: message.text == "💰 Check Prices")
    def prices_handler(message):
        coins = {
        "bitcoin": "BTC",
        "ethereum": "ETH",
        "binancecoin": "BNB",
        "solana": "SOL",
        "ripple": "XRP"}

        data = get_price()
        print(data)

        message_text = "📊 Top 5 Crypto Prices\n\n"

        for coin_id, ticker in coins.items():
            price = data[coin_id]["usd"]
            change = data[coin_id]["usd_24h_change"]

            if change > 0:
                trend_emoji = "📈"
                status_emoji = "🟢"
                sign = "+"
            elif change < 0:
                trend_emoji = "📉"
                status_emoji = "🔴"
                sign = ""
            else:
                trend_emoji = "➖"
                status_emoji = "⚪"
                sign = ""

            message_text += (
                f"💰 {ticker}: ${price:,.2f}\n"
                f"{trend_emoji} 24h: {status_emoji} {sign}{change:.2f}%\n\n"
            )

        bot.send_message(message.chat.id, message_text)


    @bot.message_handler(func=lambda message: message.text == "📝 Register")
    def register_handler(message):
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton("📱 Share Phone Number", request_contact=True)
        keyboard.add(button1)
        bot.send_message(message.chat.id, "📱 Please share your phone number:", reply_markup=keyboard)



    @bot.message_handler(content_types=["contact"])
    def contact_handler(message):
        user_id = message.from_user.id
        username = message.from_user.username
        if username:
            username = f"@{username}"
        else:
            username = "Not Set"
        first_name = message.from_user.first_name
        user_phone_number = message.contact.phone_number
        core.query.update_phone(user_id, user_phone_number)
        new_keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        my_account_button = types.KeyboardButton("👤 My Account")
        prices_button = types.KeyboardButton("💰 Check Prices")
        support_button = types.KeyboardButton("💬 Contact Support")

        new_keyb.row(my_account_button, prices_button)
        new_keyb.row(support_button)

        messagee = f"✅ Your account was created successfully!\n\n"f"🆔 User ID: {user_id}\n"f"👤 Username: {username}\n"f"📛 Name: {first_name}\n"f"📱 Phone Number: {user_phone_number}"
        bot.send_message(message.chat.id, messagee, reply_markup=new_keyb)



    @bot.message_handler(func=lambda message: message.text == "👤 My Account")
    def myaccount_handler(message):
        user_id = message.from_user.id
        user = core.query.get_user(user_id)
        if user is None:
            bot.send_message(message.chat.id, "Your account was not found ❌")
            return

        user_id, user_name, user_fname, user_lname, user_phone_number = user
        phone_number = mask_phone(user_phone_number)
        if user_name:
            user_name = f"{user_name}"
        else:
            user_name = f"Not Set"

        if not user_lname:
            user_lname = f"Not Set"

        bot.send_message(
        message.chat.id,
        f"👤 My Account\n\n"
        f"🆔 User ID: {user_id}\n"
        f"💬 Username: {user_name}\n"
        f"📛 First Name: {user_fname}\n"
        f"📛 Last Name: {user_lname}\n"
        f"📱 Phone Number: {phone_number}")


    @bot.callback_query_handler(func=lambda call: call.data == "check_membership")
    def check_membership(call):

        if is_user_member(bot, call.from_user.id):
            bot.answer_callback_query(call.id,"✅ Membership confirmed!")
            keyboardd = get_main_keyboard(call.from_user.id)
            bot.send_message(call.message.chat.id,"✅ You can now use Crypto Mehrdad.", reply_markup=keyboardd)

        else:
            bot.answer_callback_query(call.id,"❌ You haven't joined the channel yet.",show_alert=True)