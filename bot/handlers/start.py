from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from db import add_user



router = Router()

@router.message(CommandStart())
async def start(message: Message):
    lines = [
        f"Вітаю, {message.from_user.first_name}.",
        "Я - Domen Bot, тут Ви можете дізнатися інформацію про введений домен",
        "Щоб розпочати оберіть команду з меню"
    ]

    await message.answer(
        text='\n'.join(lines),
    )
    print(f'{message.from_user.username}!!!!!')
    print(f'{message.from_user.id}!!!!!')
    
    await add_user(message.from_user.id,message.from_user.username)