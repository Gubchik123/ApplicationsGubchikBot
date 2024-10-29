from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.whitelist import Removing
from utils.user_manager import UserManager
from keyboards.whitelist import make_domains_keyboard

from .menu import handle_whitelist_menu


router = Router()


@router.message(F.text.lower() == "список доменів")
async def handle_list_domains(message: Message, state: FSMContext):
    """Handles the list domains button."""
    user_data = await UserManager.get_user_data(user_id=message.from_user.id)

    if not (user_domains := user_data.get("whitelist", [])):
        await state.clear()
        await message.answer("📋 Ваш вайтлист порожній.")
        return await handle_whitelist_menu(message)
    await message.answer(
        "Виберіть домен, який хочете видалити:",
        reply_markup=await make_domains_keyboard(user_domains),
    )
    await state.set_state(Removing.domain)


@router.message(Removing.domain)
async def handle_domain_choice(message: Message, state: FSMContext):
    """Handles the domain choice."""
    if message.text == "Повернутися до меню вайтлиста":
        await state.clear()
        return await handle_whitelist_menu(message)

    try:
        await UserManager.remove_domain_from_whitelist(
            user_id=message.from_user.id, domain=message.text
        )
    except ValueError:
        return await message.answer("❌ Домен не знайдено у вашому вайтлисті.")
    await message.answer(f"✅ Домен {message.text} видалено з вайтлиста.")
    await handle_list_domains(message, state)
