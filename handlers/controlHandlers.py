from config import MAIN_COMMANDS
from utils.checkStatus import checkStatus
from utils.getInfo import get_device_info, get_device_status, post_turn_device


def register_handlers(bot, openapi, user_selected_device):
    @bot.message_handler(func=lambda message: message.text in MAIN_COMMANDS.values())
    def device_checking(message):
        command = message.text
        if not user_selected_device:
            bot.send_message(message.chat.id, ("Для начала выберите устройство: /start"))
            return

        device_id = user_selected_device[message.chat.id]
        if (command == MAIN_COMMANDS['get_status']):
            try:
                device_info = get_device_info(openapi, device_id)
                is_online = device_info.get('result', {}).get('online', False)
            except Exception as e:
                bot.send_message(message.chat.id, (f"Ошибка: {e}"))

            if not is_online:
                bot.send_message(message.chat.id, (f"Устройство не в сети 🌐❌"))
                return

            try:
                result = get_device_status(openapi, device_id)

                status_text = checkStatus(result['result'][0]['value'])
                bot.reply_to(message, f"Статус устройства: {status_text}")
            except Exception as e:
                bot.send_message(message.chat.id, (f"Ошибка: {e}"))

        if (command == MAIN_COMMANDS['device_on']):
            try:
                result = post_turn_device(openapi, device_id, True)

                status = checkStatus(result['result'][0]['value'])
                bot.reply_to(message, f"Статус устройства: {status}")
            except Exception as e:
                bot.send_message(message.chat.id, (f"Ошибка: {e}"))

        if (command == MAIN_COMMANDS['device_off']):
            try:
                result = post_turn_device(openapi, device_id, False)

                status = checkStatus(result['result'][0]['value'])
                bot.reply_to(message, f"Статус устройства: {status}")
            except Exception as e:
                bot.send_message(message.chat.id, (f"Ошибка: {e}"))
