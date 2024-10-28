import os
import json
from pathlib import Path

from dotenv import load_dotenv


load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

BASE_DIR = Path(__file__).parent.parent

USERS_FILE = BASE_DIR / "data" / "users.json"

ADMINS = [
    int(admin_chat_id) for admin_chat_id in str(os.getenv("ADMINS")).split(",")
]

# Дані проксі
USE_PROXY_1 = True
PROXY_IP_1 = ""
PROXY_PORT_1 = ""
PROXY_LOGIN_1 = ""
PROXY_PASSWORD_1 = ""

USE_PROXY_2 = True
PROXY_IP_2 = ""
PROXY_PORT_2 = ""
PROXY_LOGIN_2 = ""
PROXY_PASSWORD_2 = ""

USE_PROXY_3 = True
PROXY_IP_3 = ""
PROXY_PORT_3 = ""
PROXY_LOGIN_3 = ""
PROXY_PASSWORD_3 = ""
