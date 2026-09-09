import telebot
from telebot import *
import os
from bot.handlers import register_handlers
import requests
import core.database
from core.query import *
import logging



API_TOKEN = os.environ.get("API_TOKEN")
bot = telebot.TeleBot(API_TOKEN)


COINGECKO_API_KEY = os.environ.get("COINGECKO_API_KEY")

core.database.create_tables()

register_handlers(bot)

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s: %(message)s")
bot.infinity_polling()