import logging
import os

APP_ID = 6703198
OAUTH_URL = 'https://oauth.vk.com/authorize'
API_URL = 'https://api.vk.com/method/'
VK_URL = 'https://vk.com'
TOKEN = 'ed1271af9e8883f7a7c2cefbfddfcbc61563029666c487b2f71a5227cce0d1b533c4af4c5b888633c06ae'

current_dir = os.path.dirname(os.path.abspath(__file__))
logs_path = os.path.join(current_dir, 'logs')

if not os.path.exists(logs_path):
    os.mkdir(logs_path)

logging.basicConfig(filename="logs/debug.log", level=logging.DEBUG)
logging.basicConfig(filename="logs/warning.log", level=logging.WARNING)
logging.basicConfig(filename="logs/error.log", level=logging.ERROR)
logging.basicConfig(filename="logs/info.log", level=logging.INFO)

