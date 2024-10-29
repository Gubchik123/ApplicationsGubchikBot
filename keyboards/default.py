from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.user_manager import UserManager


async def get_menu_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Returns the keyboard for the main menu."""
    keyboard = [
        [KeyboardButton(text="🤵 Профіль")],
        [KeyboardButton(text="🚀 Запустити відправку заявок")],
        [KeyboardButton(text="🧑‍💻 Підтримка")],
        [KeyboardButton(text="🔘 Whitelist")],
    ]
    user_status = await UserManager.get_user_status(user_id)
    if user_status == "admin":
        keyboard.append([KeyboardButton(text="💠 Змінити статус")])
    return ReplyKeyboardMarkup(keyboard=keyboard, resize_keyboard=True)
