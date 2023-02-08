import asyncio
from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aioredis import Redis
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from db import BaseModel, create_async_engine, get_session_maker
from middlewares.register_check import RegisterCheck
import os

redis = RedisStorage2(
        host=os.getenv('REDIS_HOST') or '127.0.0.1'
    )

postgres_url = f"postgresql+asyncpg://{os.getenv('POSTGRES_USER')}:{os.getenv('POSTGRES_PASSWORD')}@{os.getenv('POSTGRES_HOST')}/{os.getenv('POSTGRES_DB')}"
async_engine = create_async_engine(postgres_url)
session_maker_main = get_session_maker(async_engine)

# ! Creatin Table (column schemas)
# async def create_table():
#     await proceed_schemas(async_engine, BaseModel.metadata)
# asyncio.run(create_table())
# !

bot = Bot(token=os.getenv("token"), parse_mode="HTML")

bot["db"] = session_maker_main
bot["redis"] = redis

dp = Dispatcher(bot, storage=redis)
