from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from utils.decorators import clear_state_before

from ..applications.menu import handle_applications_menu


router = Router()


@router.message(Command("applications"))
@clear_state_before
async def handle_applications_command(message: Message, state: FSMContext):
    """Handles the /applications command."""
    await handle_applications_menu(message, state)
