from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.whitelist import Adding
from utils.user_manager import UserManager
from utils.services import is_valid_, parse_domain_from_
from keyboards.whitelist import get_back_whitelist_menu_keyboard

from .menu import handle_whitelist_menu


router = Router()


@router.message(F.text.lower() == "додати домен")
async def handle_adding_domain(message: Message, state: FSMContext):
    """Handles the adding domain button."""
    user_data = await UserManager.get_user_data(user_id=message.from_user.id)
    user_domains = user_data.get("whitelist", [])

    if user_data.get("status") != "admin" and len(user_domains) >= 3:
        return await message.answer(
            "❌ Ви не можете додати більше 3-х доменів."
        )
    await message.answer(
        "📩 Відправте посилання на сайт, домен якого ви хочете додати.",
        reply_markup=await get_back_whitelist_menu_keyboard(),
    )
    await state.set_state(Adding.domain)


@router.message(Adding.domain)
async def handle_domain_input(message: Message, state: FSMContext):
    user_id = message.from_user.id
    user_input = message.text

    if not is_valid_(url=user_input):
        return await message.answer("❌ Невірний формат посилання.")
    domain = parse_domain_from_(url=user_input)
    try:
        await UserManager.append_domain_to_whitelist(
            user_id=user_id, domain=parse_domain_from_(url=user_input)
        )
    except ValueError:
        return await message.answer("❌ Цей домен вже додано до вайтлиста.")
    await message.answer(f"✅ Домен {domain} успішно додано до вайтлиста.")
    await state.clear()
    await handle_whitelist_menu(message)
