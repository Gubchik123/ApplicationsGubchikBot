from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_whitelist_menu_keyboard() -> ReplyKeyboardMarkup:
    """Returns whitelist menu keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Додати домен")],
            [KeyboardButton(text="Список доменів")],
            [KeyboardButton(text="Повернутися назад")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )


async def get_back_whitelist_menu_keyboard() -> ReplyKeyboardMarkup:
    """Returns back whitelist menu keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[[get_back_whitelist_button()]],
        resize_keyboard=True,
    )


def get_back_whitelist_button() -> KeyboardButton:
    """Returns back whitelist button."""
    return KeyboardButton(text="Повернутися до меню вайтлиста")


async def make_domains_keyboard(domains: list[str]) -> ReplyKeyboardMarkup:
    """Returns made domains keyboard."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=domain)] for domain in domains]
        + [[get_back_whitelist_button()]],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
