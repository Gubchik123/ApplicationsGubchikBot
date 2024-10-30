from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.utils.i18n import gettext as _

from utils.decorators import clear_state_before


router = Router()


@router.message(Command("help"))
@clear_state_before
async def handle_help_command(message: Message):
    """Handles the /help command."""
    await message.answer(
        "Команди бота:\n"
        "/start - Початок роботи з ботом\n"
        "/help - Отримати основні правила використання\n"
        "/menu - Отримати головне меню\n"
        "/profile - Отримати інформацію про профіль\n"
        "/support - Зв'язатися з підтримкою\n"
        "/applications - Отримати меню заявок\n"
        "/whitelist - Отримати меню вайтлиста\n"
        "/cancel - Скасувати поточну дію\n\n"
        "Раджу використати кнопки для задуманого результату\n\n"
        "Приємного використання!!!\n\n"
    )
