from typing import Union

from sqlalchemy.ext.asyncio import create_async_engine as _create_async_engine
from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker


def create_async_engine(url: Union[URL, str]) -> AsyncEngine:
    return _create_async_engine(url=url,
                         echo=False,
                         encoding='utf-8',
                         pool_pre_ping=True)

# ! ALEMBIC TAKE A CONTROLL 
# async def proceed_schemas(engine: AsyncEngine, metadata):
#     async with engine.begin() as coon:
#         await coon.run_sync(metadata.drop_all)
#         await coon.run_sync(metadata.create_all)


def get_session_maker(engine: AsyncEngine) -> sessionmaker:
    return sessionmaker(engine, class_=AsyncSession)