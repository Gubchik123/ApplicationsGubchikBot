import logging
import asyncio

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data.constants import FREQUENCIES, DURATIONS
from states.applications import Sending
from utils.tasks import request_loop
from utils.user_manager import UserManager
from utils.services import parse_domain_from_, is_valid_
from keyboards.default import get_menu_keyboard
from keyboards.applications import (
    get_back_applications_menu_keyboard,
    get_frequency_keyboard,
    get_duration_keyboard,
    get_stop_keyboard,
)

from .menu import handle_applications_menu


router = Router()


@router.message(F.text.lower() == "запустити відправку")
async def handle_applications_sending(message: Message, state: FSMContext):
    """Handles applications sending button."""
    user_id = message.from_user.id
    logging.info(f"Користувач {user_id} натиснув кнопку 'Запустити відправку'")

    if await UserManager.is_demo_limit_reached(user_id):
        return await message.answer(
            "❌ Ви вже досягли ліміту в 50 заявок. Для отримання повного доступу зверніться до адміністратора."
        )
    user_data = await UserManager.get_user_data(user_id)
    if user_data.get("status") != "demo":
        await message.answer(
            "🌐 Введіть посилання на сайт:",
            reply_markup=await get_back_applications_menu_keyboard(),
        )
    else:
        requests_to_send = 50 - user_data.get("applications_sent", 0)
        await message.answer(
            f"🌐 Ви можете надіслати ще до {requests_to_send} заявок. Введіть посилання на сайт:",
            reply_markup=await get_back_applications_menu_keyboard(),
        )
    await state.set_state(Sending.url)
    await state.update_data(
        user_id=user_id,
        user_status=user_data.get("status"),
        user_applications_sent=user_data.get("applications_sent", 0),
    )


@router.message(Sending.url)
async def handle_url_input(message: Message, state: FSMContext):
    """Handles user input of the URL."""
    url = message.text
    if not is_valid_(url):
        return await message.answer(
            "⚠️ Будь ласка, введіть коректне посилання на сайт"
        )
    domain = parse_domain_from_(url)
    users = await UserManager.get_users()
    # Перевірка, чи існує домен у вайтлісті інших користувачів
    for _, data in users.items():
        if "whitelist" in data and domain in data["whitelist"]:
            return await message.answer(
                f"❌ Домен '{domain}' вже існує у вайтлісті іншого користувача. Будь ласка, введіть інший домен."
            )
    await state.update_data(url=message.text)
    await message.answer(
        "🕰 Як швидко будуть відправлятися заявки?",
        reply_markup=await get_frequency_keyboard(),
    )
    await state.set_state(Sending.frequency)


@router.message(Sending.frequency)
async def handle_frequency_choice(message: Message, state: FSMContext):
    """Handles user choice of the frequency."""
    try:
        await state.update_data(frequency=FREQUENCIES[message.text])
    except KeyError:
        return await message.answer("⚠️ Будь ласка, оберіть один з варіантів")

    state_data = await state.get_data()
    if state_data.get("user_status") == "demo":
        await message.answer(
            "💫 Частота обрана. Вибір тривалості відправки заявок у демо статусі недоступний."
        )
        await state.update_data(duration=None)
        return await _start_sending_applications(message, state)
    await message.answer(
        "⏳ Як довго будуть відправлятися заявки?",
        reply_markup=await get_duration_keyboard(user_id=message.from_user.id),
    )
    await state.set_state(Sending.duration)


@router.message(Sending.duration)
async def handle_duration_choice(message: Message, state: FSMContext):
    """Handles user choice of the duration."""
    try:
        await state.update_data(duration=DURATIONS[message.text])
    except KeyError:
        return await message.answer("⚠️ Будь ласка, оберіть один з варіантів")
    await _start_sending_applications(message, state)


async def _start_sending_applications(message: Message, state: FSMContext):
    """Starts sending applications."""
    state_data = await state.get_data()
    await state.clear()
    await message.answer(
        f"🚀 Космічний шатл з купою заявок вже летить на сайт: {state_data['url']}",
        reply_markup=(
            await get_stop_keyboard()
            if state_data["user_status"] == "demo"
            else None
        ),
    )
    asyncio.create_task(
        request_loop(
            user_data={
                "user_id": state_data["user_id"],
                "status": state_data["user_status"],
                "applications_sent": state_data["user_applications_sent"],
            },
            url=state_data["url"],
            frequency=state_data["frequency"],
            duration=state_data["duration"],
        ),
        name=f"request_loop-user_{state_data['user_id']}_url_{state_data['url']}",
    )
    if state_data["user_status"] != "demo":
        await handle_applications_menu(message, state)


@router.message(F.text.lower() == "зупинити відправку ❌")
async def handle_stop_sending(message: Message):
    """Handles stop sending button."""
    user_id = message.from_user.id
    (task,) = [
        task
        for task in asyncio.all_tasks()
        if task.get_name().startswith(f"request_loop-user_{user_id}_")
    ]
    url = task.get_name().split("_")[-1]
    task.cancel()
    total_requests = await UserManager.increase_applications_sent(user_id, url)
    await message.answer(
        f"⭕️ Відправка заявок на {url} зупинена\n"
        f"✉️ Всього відправлено заявок: {total_requests}",
        reply_markup=await get_menu_keyboard(user_id),
    )
