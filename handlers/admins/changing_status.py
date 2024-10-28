from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.status import Status
from filters.is_admin import IsAdmin
from utils.user_manager import UserManager
from keyboards.default import get_menu_keyboard
from keyboards.admin import get_cancel_keyboard, get_status_keyboard


router = Router()


@router.message(IsAdmin(), F.text.lower() == "💠 змінити статус")
async def handle_changing_status(message: Message, state: FSMContext):
    """Handles the changing status button."""
    await message.answer(
        "👤 Введіть Telegram ID користувача, якому хочете змінити статус:",
        reply_markup=await get_cancel_keyboard(),
    )
    await state.set_state(Status.user_id)


@router.message(IsAdmin(), Status.user_id)
async def handle_user_id_input(message: Message, state: FSMContext):
    """Handles the user ID input."""
    try:
        user_id = int(message.text.strip())
        user_status = await UserManager.get_user_status(user_id)
        if not user_status:
            raise ValueError
    except ValueError:
        return await message.answer(
            "⚠️ Некоректний ID або користувач не знайдений. Спробуйте ще раз."
        )
    await state.update_data(user_id=user_id)
    await message.answer(
        f"🚦 Виберіть новий статус для користувача (Current Status: {user_status}):",
        reply_markup=await get_status_keyboard(),
    )
    await state.set_state(Status.new_status)


@router.message(IsAdmin(), Status.new_status)
async def handle_new_status_selection(message: Message, state: FSMContext):
    """Handles the new status selection."""
    if (new_status := message.text.strip()) not in ["demo", "unlim", "admin"]:
        return await message.answer(
            "⚠️ Некоректний статус. Будь ласка, виберіть із запропонованих варіантів."
        )
    state_data = await state.get_data()
    await state.clear()
    await UserManager.update_user_status(state_data["user_id"], new_status)
    await message.answer(
        f"✅ Статус користувача з ID `{state_data['user_id']}` змінено на '{new_status}'.",
        reply_markup=await get_menu_keyboard(user_id=message.from_user.id),
    )
