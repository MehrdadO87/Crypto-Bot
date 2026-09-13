import telebot
from flask import Flask, request

TOKEN = "8878913682:AAHxfrBF-ZfriL0V6Fj1Lz-aUWdjk9FdfMg"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode('utf-8'))
    bot.process_new_updates([update])
    return '', 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "سلام! بات فعاله ✅")

application = app  # Passenger این متغیر رو پیدا می‌کنه