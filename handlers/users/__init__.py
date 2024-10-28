from aiogram import Router

from .commands import commands_router
from .menu import router as menu_router
from .profile import router as profile_router
from .support import router as support_router
from .whitelist import whitelist_router


users_router = Router()

users_router.include_routers(  # ! Order is important
    commands_router,
    menu_router,
    profile_router,
    support_router,
    whitelist_router,
)
