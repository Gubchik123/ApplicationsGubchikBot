from aiogram import Router, F
from aiogram.types import Message

from keyboards.default import get_menu_keyboard


router = Router()


@router.message(F.text.lower() == "повернутися назад")
async def handle_menu(message: Message):
    """Handles main menu."""
    await message.answer(
        "🔙 Ви повернулися в головне меню.",
        reply_markup=await get_menu_keyboard(message.from_user.id),
    )
