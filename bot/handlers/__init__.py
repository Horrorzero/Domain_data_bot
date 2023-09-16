import asyncwhois
from datetime import *

from aiogram import Router,F
from aiogram.types import Message
from aiogram.filters import Command

from bot.handlers.start import router as start_router
from bot.handlers.checker import router as checker_router

router = Router()

router.include_routers(start_router, checker_router)

@router.message(Command(commands=['all_info']))
async def time_left(message: Message):
    await message.answer(text='Введіть домен сайту')
    
    @router.message(F.text.contains('com') | F.text.contains('org') | F.text.contains('ua'))
    async def site(message:Message):
        try:
            result =asyncwhois.whois_domain(message.text)

            expires = datetime.strptime((result.parser_output['expires']).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
            created = datetime.strptime((result.parser_output["created"]).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
            updated = datetime.strptime((result.parser_output["updated"]).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")

       
            print(result.parser_output)
       
            if type(result.parser_output['expires']) == list:
                date = result.parser_output['expires'][0]-datetime.now()
            else:
                date = expires-datetime.now()

            lines = [
                f'Данні домена {message.text}',
                f'Днів до кінця дії : {date.days}',
                f'Дата створення : {created}',
                f'Дата оновлення : {updated}',
                f'Хостинг домену : {result.parser_output["registrar_url"]}',
                f'Компанія хостингу : {result.parser_output["registrar"]}',
                f'Країна реєстрації : {result.parser_output["registrant_country"]}',
                f'Номер хостингу : {result.parser_output["registrar_abuse_phone"]}'
            ]
            
            await message.answer(text='\n'.join(lines))
        except:
            await message.answer(text='Не вдалося знайти данні :( \nСпробуйте ще раз або введіть інший домен!')


@router.message(Command(commands=['about']))
async def about(message:Message):
    lines = [
        "Я - Domen Bot, тут Ви можете дізнатися інформацію про введений домен",
        "Щоб дізнатися інформацію про домен введіть /all_info",   
        "Щоб нагадати строк кінця домена або доменів введіть /reminder"
    ]
    await message.answer(text='\n'.join(lines),)
    
@router.message(Command(commands=['reminder']))
async def reminder(message:Message):
    pass