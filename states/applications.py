from aiogram.fsm.state import State, StatesGroup


class Sending(StatesGroup):
    """States to start sending applications."""

    url = State()
    frequency = State()
    duration = State()
