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
USE_PROXY_1 = os.getenv("USE_PROXY_1", "0") in ("1", "t", "true", "y", "yes")
PROXY_IP_1 = os.getenv("PROXY_IP_1")
PROXY_PORT_1 = os.getenv("PROXY_PORT_1")
PROXY_LOGIN_1 = os.getenv("PROXY_LOGIN_1")
PROXY_PASSWORD_1 = os.getenv("PROXY_PASSWORD_1")

USE_PROXY_2 = os.getenv("USE_PROXY_2", "0") in ("1", "t", "true", "y", "yes")
PROXY_IP_2 = os.getenv("PROXY_IP_2")
PROXY_PORT_2 = os.getenv("PROXY_PORT_2")
PROXY_LOGIN_2 = os.getenv("PROXY_LOGIN_2")
PROXY_PASSWORD_2 = os.getenv("PROXY_PASSWORD_2")

USE_PROXY_3 = os.getenv("USE_PROXY_3", "0") in ("1", "t", "true", "y", "yes")
PROXY_IP_3 = os.getenv("PROXY_IP_3")
PROXY_PORT_3 = os.getenv("PROXY_PORT_3")
PROXY_LOGIN_3 = os.getenv("PROXY_LOGIN_3")
PROXY_PASSWORD_3 = os.getenv("PROXY_PASSWORD_3")

PROXIES = []

if USE_PROXY_1:
    PROXIES.append(
        f"http://{PROXY_LOGIN_1}:{PROXY_PASSWORD_1}@{PROXY_IP_1}:{PROXY_PORT_1}"
    )
if USE_PROXY_2:
    PROXIES.append(
        f"http://{PROXY_LOGIN_2}:{PROXY_PASSWORD_2}@{PROXY_IP_2}:{PROXY_PORT_2}"
    )
if USE_PROXY_3:
    PROXIES.append(
        f"http://{PROXY_LOGIN_3}:{PROXY_PASSWORD_3}@{PROXY_IP_3}:{PROXY_PORT_3}"
    )
