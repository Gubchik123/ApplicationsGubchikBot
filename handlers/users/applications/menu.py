from aiogram import Router, F
from aiogram.types import Message

from keyboards.applications import get_applications_menu_keyboard


router = Router()


@router.message(F.text.lower() == "🚀 відправка заявок")
@router.message(F.text.lower() == "повернутися до меню відправки заявок")
async def handle_applications_menu(message: Message):
    """Handles applications menu."""
    await message.answer(
        "Вітаю у меню відправки заявок! Виберіть дію:",
        reply_markup=await get_applications_menu_keyboard(),
    )
