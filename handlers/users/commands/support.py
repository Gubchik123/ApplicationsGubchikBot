from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command

from utils.decorators import clear_state_before

from ..support import handle_support


router = Router()


@router.message(Command("support"))
@clear_state_before
async def handle_support_command(message: Message):
    """Handles the /support command."""
    await handle_support(message)
