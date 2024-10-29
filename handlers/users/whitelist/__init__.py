from aiogram import Router

from .menu import router as menu_router
from .adding import router as adding_router
from .list import router as list_router


whitelist_router = Router()

whitelist_router.include_routers(menu_router, adding_router, list_router)
