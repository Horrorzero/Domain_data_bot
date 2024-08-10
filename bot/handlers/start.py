from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from bot.states.lang import Lang
from bot.utils.translations import translations
from bot.keyboards import localization

from db import add_user

router = Router()


@router.message(CommandStart())
async def start(message: Message, state: FSMContext):
    await state.set_state(Lang.lang)

    await add_user(message.from_user.id, message.from_user.username)

    lines = [
        'Вітаю, я - Domen Bot, тут Ви можете дізнатися інформацію про введений домен',
        "Щоб дізнатися інформацію про домен просто введіть його. Наприклад: 'Youtube.com'",
        'Щоб розпочати оберіть команду з меню'
    ]

    await message.answer(
        text='\n'.join(lines),
        reply_markup=localization.as_markup()
    )


@router.callback_query(lambda c: c.data.startswith('lang_'))
async def set_language(callback_query: CallbackQuery, state: FSMContext):
    selected_lang = callback_query.data.split('_')[1]
    await state.update_data(lang=selected_lang)

    lines = [
        translations[selected_lang]['lang_selected'],
        translations[selected_lang]['greetings'],
        translations[selected_lang]['about_domain'],
        translations[selected_lang]['menu_commands']
    ]

    await callback_query.message.edit_text("\n".join(lines))