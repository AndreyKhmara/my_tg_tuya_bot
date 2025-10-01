import os
from flask import Flask, request
import telebot

from handlers.devices import register_handlers as register_devices_handlers
from handlers.controlHandlers import register_handlers as register_control_handlers
from state import user_selected_device
from tuya_connector import TuyaOpenAPI
from config import API_ENDPOINT, ACCESS_ID, ACCESS_KEY, DEVICE_LIST
from handlers.start import register_handlers as register_start_handlers

BOT_MODE = os.getenv("BOT_MODE", "prod")  # по умолчанию "prod"
TOKEN = os.getenv("BOT_TOKEN") if BOT_MODE == "prod" else os.getenv("TEST_BOT_TOKEN")

openapi = TuyaOpenAPI(API_ENDPOINT, ACCESS_ID, ACCESS_KEY)
openapi.connect()

# Flusk для запуска бота в прод (Render/Heroku и т.п.)
# python app.py - команда запуска
# Состояния пользователей (какое устройство выбрали)

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Подключаем handlers
register_start_handlers(bot, DEVICE_LIST)
register_devices_handlers(bot, DEVICE_LIST, openapi, user_selected_device)
register_control_handlers(bot, openapi, user_selected_device)


# Главный webhook endpoint
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("UTF-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "ok", 200


@app.route("/", methods=["GET"])
def index():
    return f"Bot is running in {BOT_MODE} mode!", 200


if __name__ == "__main__":
    render_url = os.getenv("RENDER_EXTERNAL_URL")

    if render_url:  # если деплой на Render → вебхук
        WEBHOOK_URL = f"{render_url}/{TOKEN}"
        print("Webhook URL:", WEBHOOK_URL)
        bot.remove_webhook()
        bot.set_webhook(url=WEBHOOK_URL)
        app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
    else:  # если локально → polling
        print(f"Запуск в режиме polling ({BOT_MODE} mode)")
        bot.remove_webhook()
        bot.infinity_polling()
