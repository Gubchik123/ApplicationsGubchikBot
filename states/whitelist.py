from aiogram.fsm.state import State, StatesGroup


class Adding(StatesGroup):
    """States to add a domain to the whitelist."""

    domain = State()
