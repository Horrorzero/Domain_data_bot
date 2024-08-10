from aiogram import Router
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from bot.utils.domain_information import domain
from bot.filters.domain import Domain

router = Router()


@router.message(Domain())
async def site(message: Message, state: FSMContext):
    state_data = await state.get_data()
    selected_lang = state_data.get('lang', 'ua')

    text = domain(message.text, selected_lang)
    await message.answer(text=text)