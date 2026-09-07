import telebot
from telebot import *
import os
from bot.handlers import register_handlers
import requests



API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)

register_handlers(bot)


bot.infinity_polling()