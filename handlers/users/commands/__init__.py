from aiogram import Router

from .start import router as start_router


commands_router = Router()

commands_router.include_routers(start_router)
