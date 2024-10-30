from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.applications import Stopping
from keyboards.applications import get_urls_keyboard
from utils.services import (
    get_active_request_loop_task_urls,
    cancel_request_loop_task_by_,
)

from .sending import send_request_stop_message


router = Router()


@router.message(F.text.lower() == "активні сесії")
async def handle_applications_sessions(message: Message, state: FSMContext):
    """Handles applications sessions button."""
    active_urls = get_active_request_loop_task_urls(message.from_user.id)
    if not active_urls:
        return await message.answer("Наразі немає активних сесій.")
    await message.answer(
        "Оберіть сайт для зупинки відправки заявок:",
        reply_markup=await get_urls_keyboard(active_urls),
    )
    await state.set_state(Stopping.url)


@router.message(Stopping.url)
async def handle_url_input(message: Message, state: FSMContext):
    """Handles url input for stopping the request loop task."""
    url = message.text
    user_id = message.from_user.id
    if url not in get_active_request_loop_task_urls(user_id):
        return await message.answer("⚠️ Сайт не знайдено.")
    await state.clear()
    cancel_request_loop_task_by_(user_id, url)
    await send_request_stop_message(message, url)
