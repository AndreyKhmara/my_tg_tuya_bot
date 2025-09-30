import os
from flask import Flask, request
import telebot
from config import TOKEN
from handlers.devices import register_handlers as register_devices_handlers
from handlers.controlHandlers import register_handlers as register_control_handlers

from config import DEVICE_LIST

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
# Flusk для запуска бота в прод (Render/Heroku и т.п.)
# python app.py - команда запуска
# Состояния пользователей (какое устройство выбрали)
user_selected_device = {}

# Подключаем handlers
register_devices_handlers(bot, DEVICE_LIST, None, user_selected_device)
register_control_handlers(bot, DEVICE_LIST, None, user_selected_device)


# Главный webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200


@app.route("/", methods=["GET"])
def index():
    return "Bot is running!", 200

if __name__ == "__main__":
    # Укажи URL своего Render сервера
    WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_URL')}/{TOKEN}"
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
