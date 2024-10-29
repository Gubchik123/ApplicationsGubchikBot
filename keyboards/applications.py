from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


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
