from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from utils.user_manager import UserManager
from data.constants import FREQUENCIES, DURATIONS


async def get_applications_menu_keyboard() -> ReplyKeyboardMarkup:
    """Returns applications menu keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Запустити відправку")],
            [KeyboardButton(text="Активні сесії")],
            [KeyboardButton(text="Повернутися назад")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def get_back_applications_menu_keyboard() -> ReplyKeyboardMarkup:
    """Returns back applications menu keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[[get_back_applications_button()]],
        resize_keyboard=True,
    )


def get_back_applications_button() -> KeyboardButton:
    """Returns back applications button."""
    return KeyboardButton(text="Повернутися до меню відправки заявок")


async def get_frequency_keyboard() -> ReplyKeyboardMarkup:
    """Returns the keyboard for selecting the frequency."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=frequency)]
            for frequency in FREQUENCIES.keys()
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def get_duration_keyboard(user_id: int) -> ReplyKeyboardMarkup:
    """Returns the keyboard for selecting the duration."""
    durations = list(DURATIONS.keys())
    keyboard = [[KeyboardButton(text=duration)] for duration in durations[:-1]]
    user_status = await UserManager.get_user_status(user_id)
    if user_status == "admin":
        keyboard.append([KeyboardButton(text=durations[-1])])
    return ReplyKeyboardMarkup(
        keyboard=keyboard, resize_keyboard=True, one_time_keyboard=True
    )


async def get_stop_keyboard() -> ReplyKeyboardMarkup:
    """Returns the keyboard for stopping the sending."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="Зупинити відправку ❌")]],
        resize_keyboard=True,
    )


async def get_urls_keyboard(urls: list[str]) -> ReplyKeyboardMarkup:
    """Returns the keyboard for selecting the URL."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=url)] for url in urls]
        + [[get_back_applications_button()]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
