import logging
from typing import Optional

from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from data.constants import FREQUENCIES, DURATIONS
from states.applications import Sending
from utils.user_manager import UserManager
from utils.services import (
    parse_domain_from_,
    is_valid_,
    get_active_request_loop_tasks_count,
    create_request_loop_task,
    cancel_request_loop_task_for_,
)
from keyboards.applications import (
    get_back_applications_menu_keyboard,
    get_frequency_keyboard,
    get_duration_keyboard,
    get_stop_keyboard,
    get_applications_menu_keyboard,
)

from .menu import handle_applications_menu


router = Router()


@router.message(F.text.lower() == "запустити відправку")
async def handle_applications_sending(message: Message, state: FSMContext):
    """Handles applications sending button."""
    user_id = message.from_user.id
    logging.info(f"Користувач {user_id} натиснув кнопку 'Запустити відправку'")

    user_data = await UserManager.get_user_data(user_id)
    active_request_loop_tasks_count = get_active_request_loop_tasks_count(
        user_id
    )
    # Перевірка статусу користувача
    if demo_status_message := await _check_demo_status(
        user_data, active_request_loop_tasks_count
    ):
        return await message.answer(demo_status_message)
    if unlim_status_message := await _check_unlim_status(
        user_data, active_request_loop_tasks_count
    ):
        return await message.answer(unlim_status_message)
    if demo_limit_message := await _check_demo_limit(user_id):
        return await message.answer(demo_limit_message)

    await _send_message_based_on_status(message, user_data)
    await _update_state(state, user_id, user_data)


async def _check_demo_status(
    user_data: dict, active_request_loop_tasks_count: int
) -> Optional[str]:
    """Checks demo status and active request loop tasks."""
    if (
        user_data.get("status") == "demo"
        and active_request_loop_tasks_count > 0
    ):
        return "❌ Ви не можете запустити більше однієї відправки заявок одночасно у демо статусі."
    return None


async def _check_unlim_status(
    user_data: dict, active_request_loop_tasks_count: int
) -> Optional[str]:
    """Checks unlim status and active request loop tasks."""
    if (
        user_data.get("status") == "unlim"
        and active_request_loop_tasks_count >= 3
    ):
        return "❌ Ви не можете запустити більше трьох відправок заявок одночасно."
    return None


async def _check_demo_limit(user_id: int) -> Optional[str]:
    """Checks if demo limit is reached."""
    if await UserManager.is_demo_limit_reached(user_id):
        return "❌ Ви вже досягли ліміту в 50 заявок. Для отримання повного доступу зверніться до адміністратора."
    return None


async def _send_message_based_on_status(
    message: Message, user_data: dict
) -> None:
    """Sends message based on user status."""
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


async def _update_state(
    state: FSMContext, user_id: int, user_data: dict
) -> None:
    """Updates the state with user data."""
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
    create_request_loop_task(state_data)
    if state_data["user_status"] != "demo":
        await handle_applications_menu(message, state)


@router.message(F.text.lower() == "зупинити відправку ❌")
async def handle_stop_sending(message: Message):
    """Handles stop sending button."""
    await send_request_stop_message(
        message,
        url=cancel_request_loop_task_for_(user_id=message.from_user.id),
    )


async def send_request_stop_message(message: Message, url: str):
    """Sends a message about stopping the request loop task."""
    user_id = message.from_user.id
    total_requests = await UserManager.increase_applications_sent(user_id, url)
    await message.answer(
        f"⭕️ Відправка заявок на {url} зупинена\n"
        f"✉️ Всього відправлено заявок: {total_requests}",
        reply_markup=await get_applications_menu_keyboard(),
    )
