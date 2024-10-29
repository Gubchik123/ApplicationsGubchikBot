from aiogram import Dispatcher

from bot import bot
from handlers import handlers_router


dispatcher = Dispatcher()


@dispatcher.startup()
async def on_startup() -> None:
    """Runs useful functions on bot startup."""
    _register_routers()
    # await set_default_commands_for_(bot)
    # await notify_admins_on_startup_of_(bot)


def _register_routers() -> None:
    dispatcher.include_router(handlers_router)


if __name__ == "__main__":
    dispatcher.run_polling(bot)
