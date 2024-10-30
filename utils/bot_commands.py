from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeAllPrivateChats


async def set_default_commands_for_(bot: Bot) -> None:
    """Sets default bot commands."""
    await bot.set_my_commands(
        [
            BotCommand(command="start", description="Початок роботи з ботом"),
            BotCommand(
                command="help",
                description="Отримати основні правила використання",
            ),
            BotCommand(command="menu", description="Отримати головне меню"),
            BotCommand(
                command="profile",
                description="Отримати інформацію про профіль",
            ),
            BotCommand(
                command="support", description="Зв'язатися з підтримкою"
            ),
            BotCommand(
                command="applications", description="Отримати меню заявок"
            ),
            BotCommand(
                command="whitelist", description="Отримати меню вайтлиста"
            ),
            BotCommand(command="cancel", description="Скасувати поточну дію"),
        ],
        scope=BotCommandScopeAllPrivateChats(),
    )
