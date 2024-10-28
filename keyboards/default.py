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


async def get_duration_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Returns the keyboard for selecting the duration."""
    keyboard = [
        [KeyboardButton(text="1 хвилина ⏳")],
        [KeyboardButton(text="15 хвилин ⏳")],
        [KeyboardButton(text="30 хвилин ⏳")],
        [KeyboardButton(text="1 година ⏳")],
        [KeyboardButton(text="3 години ⏳")],
    ]
    user_status = await UserManager.get_user_status(user_id)
    if user_status == "admin":
        keyboard.append([KeyboardButton(text="Необмежено ⏳")])
    return ReplyKeyboardMarkup(
        keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True
    )


async def get_frequency_keyboard() -> ReplyKeyboardMarkup:
    """Returns the keyboard for selecting the frequency."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Без затримки 🚀")],
            [KeyboardButton(text="1 заявка в 10 секунд ⏳")],
            [KeyboardButton(text="1 заявка в 10 хвилин ⏳")],
            [KeyboardButton(text="1 заявка в 60 хвилин ⏳")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def get_stop_keyboard() -> ReplyKeyboardMarkup:
    """Returns the keyboard for stopping the sending."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Зупинити відправку ❌")]],
        resize_keyboard=True,
    )
