from aiogram import Bot, Dispatcher

from data.config import BOT_TOKEN
from handlers import handlers_router


bot = Bot(token=BOT_TOKEN)
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
