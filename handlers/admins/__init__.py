from aiogram import Router

from .changing_status import router as changing_status_router


admins_router = Router()

admins_router.include_routers(changing_status_router)
