from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart

from utils.user_manager import UserManager
from utils.decorators import clear_state_before
from keyboards.default import get_menu_keyboard


router = Router()


@router.message(CommandStart())
@clear_state_before
async def handle_start_command(message: Message):
    """Handles the /start command."""
    user_id = message.from_user.id
    await UserManager.register(user_id)
    await message.answer(
        "⚡️ Привіт! За допомогою цього боту ти можеш відправити заявки на будь які сайти з формою\n"
        "💎 Ми маємо різні режими з вибором тривалості та швидкості відправки заявок\n"
        "💡 Всі поля, випадаючі списки, галочки в формі на сайтах заповнюються автоматично\n"
        "🔥 Тисни кнопку нижче та запускай відправку!",
        reply_markup=await get_menu_keyboard(user_id),
    )
