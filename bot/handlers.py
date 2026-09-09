from telebot import *
from api import (
    get_top_5_prices,
    search_coin as search_coin_api,
    get_coin_data)
import core.query
from core.membership import is_user_member, join_channel_markup
import time
import threading

_last_request_lock = threading.Lock()
user_last_request = {}


def get_main_keyboard(user_id):
    phone_number = core.query.get_user_phone(user_id)
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    prices_button = types.KeyboardButton("💰 Check Prices")
    support_button = types.KeyboardButton("💬 Contact Support")
    search_button = types.KeyboardButton("🔍 Search Coin")
    keyboard.row(prices_button, search_button)
    if phone_number:
        account_button = types.KeyboardButton("👤 My Account")
        keyboard.row(account_button,support_button)
    else:
        register_button = types.KeyboardButton("📝 Creat Account")
        keyboard.row(register_button,support_button)
    return keyboard


def mask_phone(phone_number):
    if not phone_number:
        return "Not set"

    if len(phone_number) <= 7:
        return "*" * len(phone_number)

    return phone_number[:3] + "*" * (len(phone_number) - 6) + phone_number[-3:]


def format_change(change):
    if change > 0:
        return f"📈 🟢 +{change:.2f}%"
    elif change < 0:
        return f"📉 🔴 {change:.2f}%"
    else:
        return "➖ ⚪ 0.00%"



def register_handlers(bot: TeleBot):
    def anti_spam(message):
        user_id = message.from_user.id
        now = time.time()

        with _last_request_lock:
            last_request = user_last_request.get(user_id)
            if last_request and now - last_request < 1:
                return False
            user_last_request[user_id] = now

        return True

    
    @bot.message_handler(commands=['start'])
    def start_handler(message):
        
        if not anti_spam(message):
            return
        
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

        core.query.insert_user(user_id,user_name,user_fname,user_lname)

        markup = get_main_keyboard(user_id)
        bot.send_message(message.chat.id, """Welcome to Crypto Mehrdad!👋

    📈 Get the latest cryptocurrency prices quickly and easily.

    - Check the top 5 cryptocurrencies
    - View real-time prices
    - Simple and fast

    Use the buttons below to get started.""", reply_markup=markup)

    @bot.message_handler(commands=['help'])
    def help_handler(message):
        if not is_user_member(bot, message.from_user.id):
            bot.send_message(message.chat.id,"🔒 To use Crypto Mehrdad, please join our channel first.",reply_markup=join_channel_markup())
            return
        
        message_help = ("📖 Help\n\n"
        "💰 Check Prices\n"
        "View the latest prices of the top 5 cryptocurrencies.\n\n"
        "🔍 Search Coin\n"
        "Search for any cryptocurrency by name or symbol.\n\n"
        "💬 Contact Support\n"
        "Contact our support team if you need help.\n\n"
        "📝 Creat Account\n"
        "Create your account by sharing your phone number.\n\n"
        "👤 My Account\n"
        "View your account information.\n\n")
        bot.send_message(message.chat.id, message_help)


    @bot.message_handler(func=lambda message: message.text == "💬 Contact Support")
    def sopport_handler(message):

        if not anti_spam(message):
            return
        
        bot.send_message(message.chat.id, "If you have any questions, problems or suggestions, feel free to contact our support team.\n\n💬 Support: @Mehrdaddg69\n\nWe'll be happy to help!")



    @bot.message_handler(func=lambda message: message.text == "💰 Check Prices")
    def prices_handler(message):

        if not anti_spam(message):
                    return
        
        coins = {
            "bitcoin": "BTC",
            "ethereum": "ETH",
            "binancecoin": "BNB",
            "solana": "SOL",
            "ripple": "XRP"
        }

        data = get_top_5_prices()

        if isinstance(data, dict) and "error" in data:

            if data["error"] == "rate_limit":
                bot.send_message(
                    message.chat.id,
                    "⚠️ Too many requests. Please try again later."
                )

            elif data["error"] == "timeout":
                bot.send_message(
                    message.chat.id,
                    "⚠️ Request timed out. Please try again."
                )

            else:
                bot.send_message(
                    message.chat.id,
                    "⚠️ Network error. Please try again later."
                )

            return

        message_text = "📊 Top 5 Crypto Prices\n\n"

        for coin_id, ticker in coins.items():

            coin = next(
                item for item in data
                if item["id"] == coin_id
            )
            if coin is None:
                 continue

            price = coin["current_price"]

            change_24h = coin.get(
                "price_change_percentage_24h_in_currency"
            ) or 0

            change_7d = coin.get(
                "price_change_percentage_7d_in_currency"
            ) or 0

            change_30d = coin.get(
                "price_change_percentage_30d_in_currency"
            ) or 0

            change_1y = coin.get(
                "price_change_percentage_1y_in_currency"
            ) or 0

            message_text += (
                f"💰 {ticker}: ${price:,.2f}\n"
                f"📊 24h: {format_change(change_24h)}\n"
                f"📊 7d: {format_change(change_7d)}\n"
                f"📊 1M: {format_change(change_30d)}\n"
                f"📊 1Y: {format_change(change_1y)}\n\n")

        bot.send_message(message.chat.id,message_text)


    @bot.message_handler(func=lambda message: message.text == "📝 Creat Account")
    def register_handler(message):

        if not anti_spam(message):
                    return
        
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
        button1 = types.KeyboardButton("📱 Share Phone Number", request_contact=True)
        keyboard.add(button1)
        bot.send_message(message.chat.id, "📱 Please share your phone number:", reply_markup=keyboard)



    @bot.message_handler(content_types=["contact"])
    def contact_handler(message):

        if not anti_spam(message):
                    return
        
        user_id = message.from_user.id
        username = message.from_user.username
        if username:
            username = f"@{username}"
        else:
            username = "Not Set"
        first_name = message.from_user.first_name
        user_phone_number = message.contact.phone_number
        core.query.update_phone(user_id, user_phone_number)
        # new_keyb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        # my_account_button = types.KeyboardButton("👤 My Account")
        # prices_button = types.KeyboardButton("💰 Check Prices")
        # support_button = types.KeyboardButton("💬 Contact Support")

        # new_keyb.row(🔍 Search Coin, prices_button)
        # new_keyb.row(my_account_button, support_button)
        new_keyb = get_main_keyboard(user_id)
        phone_number = mask_phone(user_phone_number)
        messagee = f"✅ Your account was created successfully!\n\n"f"🆔 User ID: {user_id}\n"f"👤 Username: {username}\n"f"📛 Name: {first_name}\n"f"📱 Phone Number: {phone_number}"
        bot.send_message(message.chat.id, messagee, reply_markup=new_keyb)



    @bot.message_handler(func=lambda message: message.text == "👤 My Account")
    def myaccount_handler(message):

        if not anti_spam(message):
                    return
        
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




    @bot.message_handler(func=lambda message: message.text == "🔍 Search Coin")
    def search_handler(message):

        if not anti_spam(message):
                    return
        
        bot.send_message(message.chat.id, "🔍 Enter The coin name or symbol:")
        bot.register_next_step_handler(message, process_search)



    def process_search(message):

        if not anti_spam(message):
                    return
        
        query = message.text.strip()

        if not query:
            bot.send_message(message.chat.id,"❌ Please enter a valid coin name or symbol.")
            return

        results = search_coin_api(query)

        if isinstance(results, dict) and "error" in results:

            if results["error"] == "rate_limit":
                bot.send_message(message.chat.id,"⚠️ Too many requests. Please try again later.")

            elif results["error"] == "timeout":
                bot.send_message(message.chat.id,"⚠️ Request timed out. Please try again.")

            else:
                bot.send_message(message.chat.id,"⚠️ Network error. Please try again later.")
            return

        coins = results.get("coins", [])

        if not coins:
            bot.send_message(message.chat.id,"❌ No coin found.")
            return

        coin = coins[0]

        coin_id = coin["id"]
        coin_name = coin["name"]
        symbol = coin["symbol"].upper()

        data = get_coin_data(coin_id)

        if isinstance(data, dict) and "error" in data:

            if data["error"] == "rate_limit":
                bot.send_message(message.chat.id,"⚠️ Too many requests. Please try again later.")

            elif data["error"] == "timeout":
                bot.send_message(message.chat.id,"⚠️ Request timed out. Please try again.")

            else:
                bot.send_message(message.chat.id,"⚠️ Network error. Please try again later.")
            return

        if data is None:
            bot.send_message(message.chat.id,"❌ Couldn't get information for this coin.")
            return

        price = data["current_price"]

        change_24h = data.get("price_change_percentage_24h_in_currency") or 0

        change_7d = data.get("price_change_percentage_7d_in_currency") or 0

        change_30d = data.get("price_change_percentage_30d_in_currency") or 0

        change_1y = data.get("price_change_percentage_1y_in_currency") or 0
        message_text = (
            f"🪙 {coin_name} ({symbol})\n\n"
            f"💰 Price: ${price:,.2f}\n"
            f"📊 24h: {format_change(change_24h)}\n"
            f"📊 7d: {format_change(change_7d)}\n"
            f"📊 1M: {format_change(change_30d)}\n"
            f"📊 1Y: {format_change(change_1y)}")
        bot.send_message(message.chat.id,message_text, reply_markup=get_main_keyboard(message.from_user.id))