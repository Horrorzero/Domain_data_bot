import logging
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import Bot, Dispatcher
from bot.handlers import router

from dotenv import load_dotenv
import os

from bot.logic import get_expires

logging.basicConfig(level=logging.INFO)

load_dotenv()


async def main():
    bot = Bot(token=os.environ.get('BOT_TOKEN'))
    dp = Dispatcher()
    dp.include_router(router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_expires, "interval", seconds=10,
                      start_date='2022-05-14 17:25:00')
    scheduler.start()

    await dp.start_polling(bot)
    
if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    loop.run_until_complete(main())