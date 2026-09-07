from telebot import types


CHANNEL_ID = -1004205241131
CHANNEL_USERNAME = "https://t.me/bottest12134"


def is_user_member(bot, user_id):
    try:
        member = bot.get_chat_member(CHANNEL_ID, user_id)
        return member.status in ["member","administrator","creator"]
    except Exception:
        return False


def join_channel_markup():
    markup = types.InlineKeyboardMarkup()
    join_button = types.InlineKeyboardButton("📢 Join Our Channel",url=CHANNEL_USERNAME)
    check_button = types.InlineKeyboardButton("✅ I Joined",callback_data="check_membership")

    markup.add(join_button)
    markup.add(check_button)

    return markup