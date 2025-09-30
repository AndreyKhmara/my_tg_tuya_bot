from telebot import TeleBot
from tuya_connector import TuyaOpenAPI
from handlers import (start, devices, controlHandlers)
from state import user_selected_device
# команда для запуска при локальной разработке - python main.py
from config import TOKEN, API_ENDPOINT, ACCESS_ID, ACCESS_KEY, DEVICE_LIST

bot = TeleBot(TOKEN)

openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

start.register_handlers(bot, DEVICE_LIST)
devices.register_handlers(bot, DEVICE_LIST, openapi, user_selected_device)
controlHandlers.register_handlers(bot, DEVICE_LIST, openapi, user_selected_device)

bot.infinity_polling()
