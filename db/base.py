from contextlib import asynccontextmanager
from collections.abc import AsyncIterator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from dotenv import load_dotenv
import os

load_dotenv()

engine = create_async_engine(os.environ.get('DB_URL'), echo=True)
Base = declarative_base()

def async_session_generator():
    return sessionmaker[AsyncSession](
        engine,
        class_=AsyncSession,
        expire_on_commit=False,
    )
        
@asynccontextmanager
async def get_session() -> AsyncIterator[AsyncSession]:
    try:
        async_session = async_session_generator()

        async with async_session() as session:
            yield session
    except:
        await session.rollback()
        raise
    finally:
        await session.close()