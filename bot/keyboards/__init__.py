from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

from bot.utils.translations import translations


def show_my_domains(selected_lang: str):
    kb = [
        KeyboardButton(text=f'{translations[selected_lang]["my_domains"]}')
    ]

    return ReplyKeyboardMarkup(keyboard=[kb], resize_keyboard=True)


def domain_actions(lang):
    domains_actions = InlineKeyboardBuilder()

    delete_domains = InlineKeyboardButton(text=f'{translations[lang]["delete"]}', callback_data='delete')
    delete_all = InlineKeyboardButton(text=f'{translations[lang]["delete_all"]}', callback_data='all')

    domains_actions.add(delete_domains, delete_all)
    
    domains_actions.adjust(2, 1)
    
    return domains_actions.as_markup()


localization = InlineKeyboardBuilder()

lang_ua = InlineKeyboardButton(text='Українська', callback_data='lang_ua')
lang_en = InlineKeyboardButton(text='English', callback_data='lang_en')

localization.add(lang_ua, lang_en)

localization.adjust(2)
