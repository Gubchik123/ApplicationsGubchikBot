from aiogram import Router

from .menu import router as menu_router


whitelist_router = Router()

whitelist_router.include_routers(menu_router)
