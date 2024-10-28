from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import clear_state_before

from ..profile import handle_profile


router = Router()


@router.message(Command("profile"))
@clear_state_before
async def handle_profile_command(message: Message):
    """Handles the /profile command."""
    await handle_profile(message)
