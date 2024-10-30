from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states.applications import Stopping
from utils.user_manager import UserManager
from keyboards.default import get_menu_keyboard
from keyboards.applications import get_urls_keyboard
from utils.services import (
    get_active_request_loop_task_urls,
    cancel_request_loop_task_by_,
)


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
    total_requests = await UserManager.increase_applications_sent(user_id, url)
    await message.answer(
        f"⭕️ Відправка заявок на {url} зупинена\n"
        f"✉️ Всього відправлено заявок: {total_requests}",
        reply_markup=await get_menu_keyboard(user_id),
    )
