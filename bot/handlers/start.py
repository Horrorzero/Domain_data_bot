from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

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