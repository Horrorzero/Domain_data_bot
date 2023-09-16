import logging

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot.handlers import router

import asyncio

from bot.config import BOT_TOKEN

logging.basicConfig(level=logging.INFO)


async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher()
    dp.include_router(router)

        
    await dp.start_polling(bot)
    
if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    loop.run_until_complete(main())