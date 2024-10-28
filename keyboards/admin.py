from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


async def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """Returns the keyboard with the cancel button."""
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="/cancel")]],
        resize_keyboard=True,
    )


async def get_status_keyboard() -> ReplyKeyboardMarkup:
    """Returns the keyboard with the status buttons."""
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="demo")],
            [KeyboardButton(text="unlim")],
            [KeyboardButton(text="admin")],
        ],
        resize_keyboard=True,
        one_time_keyboard=True,
    )
