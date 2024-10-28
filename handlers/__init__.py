from aiogram import Router

from .admins import admins_router
from .users import users_router
from .users.other import router as other_router


handlers_router = Router()

handlers_router.include_routers(  # ! Order is important
    users_router, admins_router, other_router
)
