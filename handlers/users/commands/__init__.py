from aiogram import Router

from .start import router as start_router
from .menu import router as menu_router
from .profile import router as profile_router
from .support import router as support_router
from .applications import router as applications_router
from .whitelist import router as whitelist_router


commands_router = Router()

commands_router.include_routers(
    start_router,
    menu_router,
    profile_router,
    support_router,
    applications_router,
    whitelist_router,
)
