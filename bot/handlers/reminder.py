from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.filters.domain import Domain
from bot.keyboards import show_my_domains, domain_actions
from bot.bot import bot
from bot.utils.translations import translations
from bot.states.actions import Actions

from db import add_domains, delete_all_domains, delete_domains, show_domains

router = Router()


@router.message(Command(commands=['reminder']))
async def reminder(message: Message, state: FSMContext):
    state_data = await state.get_data()
    selected_lang = state_data.get('lang', 'ua')

    await message.answer(text=translations[selected_lang]['enter_domains'])
    await state.set_state(Actions.waiting_for_action)


@router.message(Actions.waiting_for_action, Domain())
async def domains(message: Message, state: FSMContext):
    state_data = await state.get_data()
    selected_lang = state_data.get('lang', 'ua')

    domains = str(set((message.text).split()))

    result = await add_domains(domains, message.from_user.username)

    if result is False:
        return await message.answer(text=translations[selected_lang]['unsuccessful_saving'])

    await state.clear()
    return await message.answer(text=translations[selected_lang]['successful_saving'],
                         reply_markup=show_my_domains(selected_lang))


@router.message((F.text == 'Мої домени') | (F.text == 'My domains'))
async def my_domains(message: Message, state: FSMContext):
    state_data = await state.get_data()
    selected_lang = state_data.get('lang', 'ua')

    try:
        domains = await show_domains(message.from_user.id)
        await message.answer(text=f"{translations[selected_lang]['show_domains']} {''.join(domains)}",
                             reply_markup=domain_actions(selected_lang))

    except Exception as e:
        print(e)
        await message.answer(text=translations[selected_lang]['unsaved_domains'])


@router.callback_query()
async def actions(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    selected_lang = state_data.get('lang', 'ua')

    if callback.data == 'delete':
        await bot.send_message(chat_id=callback.message.chat.id, text=translations[selected_lang]['domain_removal'])
        await state.set_state(Actions.waiting_for_domains_to_delete)

    elif callback.data == 'all':
        await delete_all_domains(callback.from_user.username)
        await bot.send_message(chat_id=callback.message.chat.id, text=translations[selected_lang]['successful_removal'])


@router.message(Actions.waiting_for_domains_to_delete)
async def delete(message: Message, state: FSMContext):
    state_data = await state.get_data()
    selected_lang = state_data.get('lang', 'ua')

    domains = list(message.text.split(' '))
    output = await delete_domains(message.from_user.username, domains, selected_lang)
    await message.answer(text=output)
