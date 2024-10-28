from aiogram.filters import Filter
from aiogram.types import Message, CallbackQuery

from utils.user_manager import UserManager


class IsAdmin(Filter):
    """Filter for checking if user is admin."""

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        """Returns True if user is admin and False otherwise."""
        user_status = await UserManager.get_user_status(event.from_user.id)
        return user_status == "admin"
