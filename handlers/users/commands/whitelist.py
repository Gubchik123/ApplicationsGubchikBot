from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.decorators import clear_state_before

from ..whitelist.menu import handle_whitelist_menu


router = Router()


@router.message(Command("whitelist"))
@clear_state_before
async def handle_whitelist_command(message: Message, state: FSMContext):
    """Handles the /whitelist command."""
    await handle_whitelist_menu(message, state)
