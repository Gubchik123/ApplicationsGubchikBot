from aiogram.fsm.state import State, StatesGroup


class Status(StatesGroup):
    """States to change an user status."""

    user_id = State()
    new_status = State()
