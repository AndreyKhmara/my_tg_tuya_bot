from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def register_handlers(bot, DEVICE_LIST):
    @bot.message_handler(commands=['start'])
    def send_welcome(message):
        markup = InlineKeyboardMarkup()
        for device_name in DEVICE_LIST.keys():
            markup.add(InlineKeyboardButton(text=device_name, callback_data=f"{DEVICE_LIST[device_name]}"))

        bot.send_message(
            message.chat.id,
            "Привет 👋\nВыберите устройство:",
            reply_markup=markup
        )
