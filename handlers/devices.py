from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config import MAIN_COMMANDS


def register_handlers(bot, DEVICE_LIST, openapi, user_selected_device):
    @bot.callback_query_handler(func=lambda call: call.data and call.data in DEVICE_LIST.values())
    def handle_device_selection(call):
        device_id = call.data

        device_name = next((k for k, v in DEVICE_LIST.items() if v == device_id), None)

        if not device_name:
            bot.answer_callback_query(call.id, "Неизвестное устройство ⚠️")
            return
        if device_name:
            user_selected_device[call.from_user.id] = device_id
            markup = ReplyKeyboardMarkup(row_width=3)

            for command in MAIN_COMMANDS.values():
                item_button = KeyboardButton(command)
                markup.add(item_button)
            bot.send_message(call.message.chat.id, f"Вы выбрали {device_name} ✅", reply_markup=markup)
            bot.answer_callback_query(call.id)
