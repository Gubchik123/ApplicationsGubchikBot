from aiogram import Router, F
from aiogram.types import Message


router = Router()


@router.message(F.text.lower() == "🧑‍💻 підтримка")
async def handle_support(message: Message):
    """Handles the support button."""
    await message.answer("✉️ Для звʼязку з нами звертайтеся до...")
