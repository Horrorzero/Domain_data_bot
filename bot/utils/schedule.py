from datetime import datetime
import asyncwhois
import asyncio

from db.models import User, Domain
from db.base import get_session

from sqlalchemy import select

from bot.bot import bot
from bot.utils.logic import editor


async def get_expires():
    async with get_session() as session:
        all_domains_query = select(Domain.name)
        all_domains = (await session.scalars(all_domains_query)).all()

        tasks = []

        for a in all_domains:
            user_id_query = select(Domain.user_id).where(Domain.name == a)
            user_id = (await session.execute(user_id_query)).scalar()

            user_query = select(User.tg_id).where(User.id == user_id)
            user_tg_id = (await session.execute(user_query)).scalar()

            domain_query = select(Domain.name).where(Domain.user_id == user_id)
            domains = (await session.scalars(domain_query)).all()

            domains = editor(" ".join(domains))
            domains = domains.split()

            for d in domains:
                tasks.append(check_domain_expiry(d, user_tg_id))

        await asyncio.gather(*tasks)


async def check_domain_expiry(domain_name, user_tg_id):
    result = asyncwhois.whois_domain(domain_name)

    expires = result.parser_output.get('expires')
    if isinstance(expires, list):
        date = expires[0] - datetime.now()
    else:
        expires = datetime.strptime(expires.strftime("%Y/%m/%d %H:%M:%S"), "%Y/%m/%d %H:%M:%S")
        date = expires - datetime.now()

    await bot.send_message(chat_id=user_tg_id, text=f'Днів до кінця строку дії домена \n{domain_name}: {date.days}')
