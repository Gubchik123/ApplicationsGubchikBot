import logging

from typing import Callable

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery


def clear_state_before(handler: Callable) -> Callable:
    """Decorator to clear state before handler execution."""

    async def wrapper(
        event: Message | CallbackQuery, state: FSMContext
    ) -> None:
        """Clears state before handler execution."""
        current_state = await state.get_state() if state else None

        if current_state is not None:
            logging.info(f"Cancelling state {current_state}")
            await state.clear()

        try:
            await handler(event, state)
        except TypeError:
            await handler(event)

    return wrapper
