from aiogram import Router

from .menu import router as menu_router
from .sending import router as sending_router


applications_router = Router()

applications_router.include_routers(menu_router, sending_router)
