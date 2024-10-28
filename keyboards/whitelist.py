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
