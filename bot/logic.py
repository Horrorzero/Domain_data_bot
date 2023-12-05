from datetime import datetime
import asyncwhois

# async def foo():
#     print(f'{datetime.now()} Foo')
from aiogram.types import Message
from db.models import User, Domain
from db.base import get_session

from sqlalchemy import select


async def get_expires():
    async with get_session() as session:
        all_domains_query =  select(Domain.name)
        all_domains = (await session.scalars(all_domains_query)).all()
        for a in all_domains:
            print(a)

