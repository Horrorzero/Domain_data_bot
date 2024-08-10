from aiogram import Router

from bot.handlers.checker import router as checker_router
from bot.handlers.help import router as help_router
from bot.handlers.start import router as start_router
from bot.handlers.all_info import router as info_router
from bot.handlers.reminder import router as reminder_router

router = Router()

router.include_routers(
    reminder_router,
    info_router,
    start_router,
    help_router,
    checker_router
)