from aiogram import Router

from .users import users_router


handlers_router = Router()

handlers_router.include_routers(users_router)
