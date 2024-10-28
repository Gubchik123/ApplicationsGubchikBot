from aiogram import Router

from .commands import commands_router
from .menu import menu_router


users_router = Router()

users_router.include_routers(commands_router, menu_router)
