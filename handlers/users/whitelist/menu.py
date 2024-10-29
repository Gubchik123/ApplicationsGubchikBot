from aiogram import Router, F
from aiogram.types import Message

from utils.user_manager import UserManager
from utils.decorators import clear_state_before
from keyboards.whitelist import get_whitelist_menu_keyboard


router = Router()


@router.message(F.text.lower() == "🔘 whitelist")
@router.message(F.text.lower() == "повернутися до меню вайтлиста")
@clear_state_before
async def handle_whitelist_menu(message: Message):
    """Handles whitelist menu."""
    user_status = await UserManager.get_user_status(
        user_id=message.from_user.id
    )
    if user_status == "demo":
        return await message.answer(
            "❌ Ця функція доступна тільки у платній версії боту."
        )
    await message.answer(
        "Вітаю у меню вайтлисту! Виберіть дію:",
        reply_markup=await get_whitelist_menu_keyboard(),
    )
