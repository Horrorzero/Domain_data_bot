import asyncio
from datetime import datetime, timedelta

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Dispatcher

from bot.handlers import router
from bot.utils.schedule import get_expires
from bot.bot import bot
from bot.logger import get_logger

logger = get_logger(__name__)


async def main():
    dp = Dispatcher()

    dp.include_router(router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_expires, "date", run_date=datetime.now() + timedelta(days=30))
    scheduler.start()

    await dp.start_polling(bot)


if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    loop.run_until_complete(main())
