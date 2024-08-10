from aiogram import Router
from aiogram.types import Message

from bot.bot import bot

router = Router()


@router.message()
async def checker(message: Message):
    await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
