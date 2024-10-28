from aiogram import Router

from .start import router as start_router
from .menu import router as menu_router


commands_router = Router()

commands_router.include_routers(start_router)
