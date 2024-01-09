from datetime import datetime
import asyncwhois


from aiogram.types import Message
from aiogram import Bot

from db.models import User, Domain
from db.base import get_session

from sqlalchemy import select

from dotenv import load_dotenv
import os

load_dotenv()

bot = Bot(token=os.environ.get('BOT_TOKEN'))

async def get_expires():
    async with get_session() as session:
        
        all_domains_query =  select(Domain.name)
        all_domains = (await session.scalars(all_domains_query)).all()
        
        for a in all_domains:
            user_id_query = select(Domain.user_id).where(a == Domain.name)
            user_id_query = (await session.execute(user_id_query)).scalar()
            
            user_query = select(User.tg_id).where(user_id_query == User.id)
            users = (await session.execute(user_query)).scalar()
            
            domain_query = select(Domain.name).where(user_id_query == Domain.user_id)
            domains = (await session.execute(domain_query)).scalar()
            
            domains = domains.replace('{','')
            domains = domains.replace('}','')
            domains = domains.replace('\'','')
            domains = domains.replace(',','')
            domains = domains.split()
            
           
            for d in domains:
                result = asyncwhois.whois_domain(d)

                expires = datetime.strptime((result.parser_output['expires']).strftime("%Y/%m/%d %H:%M:%S"),"%Y/%m/%d %H:%M:%S")
                date = expires-datetime.now()
                
                await bot.send_message(chat_id=users, text=f'Днів до кінця строку дії домена \n{d}: {date.days}')
            