from aiogram import Router
from aiogram.types import Message
from aiogram.exceptions import TelegramBadRequest


router = Router()


@router.message()
async def handle_all_other_messages(message: Message):
    """Handles all other messages."""
    try:
        await message.answer(
            "Я Вас не розумію :(\n"
            "Раджу використати кнопки або команди для задуманого результату."
        )
    except TelegramBadRequest:
        pass
