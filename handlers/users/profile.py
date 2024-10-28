from datetime import datetime

from aiogram import Router, F
from aiogram.types import Message

from utils.user_manager import UserManager
from data.constants import STATUS_TRANSLATION


router = Router()


@router.message(F.text.lower() == "🤵 профіль")
async def handle_profile(message: Message):
    user_id = message.from_user.id
    user_data = await UserManager.get_user_data(user_id)
    registration_date = user_data.get("registration_date")

    if not registration_date:
        await message.answer("⚠️ Ви не зареєстровані. Напишіть боту /start")
        return
    status = user_data.get("status", "N/A")
    translated_status = STATUS_TRANSLATION.get(status, status)
    days_since_registration = (
        datetime.now() - datetime.fromisoformat(registration_date)
    ).days
    await message.answer(
        f"<b>🤵 Ваш профіль</b>\n\n"
        f"📊 Ваш статус: {translated_status}\n"
        f"🪪 Ваш Telegram ID: <code>{user_id}</code>\n"
        f"🥇 Ми разом вже {days_since_registration} днів\n"
        f"📩 Загалом надіслано заявок: {user_data.get('applications_sent', 0)}",
        parse_mode="HTML",
    )
