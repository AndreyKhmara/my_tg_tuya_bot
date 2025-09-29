import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv('BOT_TOKEN')  # токен бота

ACCESS_ID = os.getenv('ACCESS_ID')
ACCESS_KEY = os.getenv('ACCESS_KEY')
API_ENDPOINT = os.getenv('API_ENDPOINT')  # смотри регион: eu, us, cn

DEVICE_ID_1 = os.getenv('DEVICE_ID_1') # id устройства

MAIN_COMMANDS = {
    "get_status": "GET_STATUS",
    "device_on": "DEVICE_ON",
    "device_off": "DEVICE_OFF",
}

DEVICE_LIST = {
    "garage_light": DEVICE_ID_1,
}
