from aiogram import Dispatcher

from bot import bot
from handlers import handlers_router
from utils.bot_commands import set_default_commands_for_


dispatcher = Dispatcher()


@dispatcher.startup()
async def on_startup() -> None:
    """Runs useful functions on bot startup."""
    dispatcher.include_router(handlers_router)

    await set_default_commands_for_(bot)


if __name__ == "__main__":
    dispatcher.run_polling(bot)
