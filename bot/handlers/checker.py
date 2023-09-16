from aiogram import Router
from aiogram.types import Message

router = Router()

@router.message()
async def checker(message:Message):
    await message.reply('Я вас не зрозумів :(')