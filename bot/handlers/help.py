from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.utils.translations import translations

router = Router()


@router.message(Command(commands=['help']))
async def help(message: Message, state: FSMContext):
    state_data = await state.get_data()
    selected_lang = state_data.get('lang', 'ua')

    lines = [
        translations[selected_lang]['about_domain'],
        translations[selected_lang]['help_text'],
    ]

    await message.answer(text='\n'.join(lines))
