import logging
import asyncio

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from aiogram import  Dispatcher
from bot.handlers import router

from bot.logic import get_expires, bot

logging.basicConfig(level=logging.INFO)




async def main():
    dp = Dispatcher()
    dp.include_router(router)

    scheduler = AsyncIOScheduler()
    scheduler.add_job(get_expires, "interval", seconds=10)
    scheduler.start()

    await dp.start_polling(bot)
    
if __name__ == '__main__':
    loop = asyncio.new_event_loop()

    loop.run_until_complete(main())