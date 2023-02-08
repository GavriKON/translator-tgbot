import json
from aiogram.contrib.fsm_storage.redis import RedisStorage2
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.attributes import flag_modified
from sqlalchemy.exc import ProgrammingError
from sqlalchemy import select, update, insert
from db.User import User

async def get_user(telegram_id: int, session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            res = await session.stream(select(User).where(User.telegram_user_id == telegram_id))
            async for cell in res.scalars():
                session.expunge_all()
                return cell

async def is_user_exists(telegram_id: int, session_maker: sessionmaker, redis: RedisStorage2) -> bool:
    res = await redis.get_data(user='is_user_exists:' + str(telegram_id))
    if not res:
        async with session_maker() as session:
            async with session.begin():
                sql_res = await session.execute(select(User).where(User.telegram_user_id == telegram_id))
                await redis.set_data(user='is_user_exists:' + str(telegram_id), data=1 if sql_res else 0)
                return bool(res)
    else:
        return bool(res)

async def add_user(telegram_id: int, session_maker:sessionmaker) -> None:
    async with session_maker() as session:
        async with session.begin():
            
            user = User(telegram_user_id=telegram_id)
            try:
                await session.merge(user)
                await session.commit()
            except ProgrammingError as ex:
                pass

async def commit_bot_language(telegram_id: int, language: str, session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            res = update(User).where(User.telegram_user_id == telegram_id).values(bot_language=language)
            await session.execute(res)
            await session.commit()

async def commit_translation_language(telegram_id: int, language: str, session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            res = update(User).where(User.telegram_user_id == telegram_id).values(translation_language=language)
            await session.execute(res)
            await session.commit()

async def commit_dictionary(telegram_id: int, data: dict, session_maker:sessionmaker = None):
    async with session_maker() as session:
        async with session.begin():
            res = await session.stream(select(User).where(User.telegram_user_id == telegram_id))
            async for row in res.scalars():
                if row.dictionary != {}:
                    row.dictionary['dictionary'].append(data)
                    flag_modified(row, "dictionary")
                    session.add(row)
                else:
                    row.dictionary['dictionary'] = []
                    row.dictionary['dictionary'].append(data)
                    flag_modified(row, "dictionary")
                    session.add(row)
                await session.commit()

async def alocate_dictionary(telegram_id: int, session_maker:sessionmaker = None):
    async with session_maker() as session:
        async with session.begin():
            res = await session.stream(select(User).where(User.telegram_user_id == telegram_id))
            async for row in res.scalars():
                if row.dictionary != {}:
                    return None
                else:
                    row.dictionary['dictionary'] = []
                    flag_modified(row, "dictionary")
                    session.add(row)
                await session.commit()

async def delete_from_dictionary(telegram_id: int, data: dict, session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            res = await session.stream(select(User).where(User.telegram_user_id == telegram_id))
            async for row in res.scalars():
                del row.dictionary['dictionary'][data]
                flag_modified(row, "dictionary")
                session.add(row)
                await session.commit()

async def get_user_dictionary(telegram_id: int, session_maker:sessionmaker) -> dict:
    async with session_maker() as session:
        async with session.begin():
            res = await session.stream(select(User).where(User.telegram_user_id == telegram_id))
            async for row in res.scalars():
                return row.dictionary

async def clear_all_dictionary(telegram_id: int, session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            res = await session.stream(select(User).where(User.telegram_user_id == telegram_id))
            async for row in res.scalars():
                row.dictionary['dictionary'].clear()
                flag_modified(row, "dictionary")
                session.add(row)
                await session.commit()

async def take_all_users(session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            res = await session.stream(select(User))
            async for row in res.scalars():
                return row.user_id

async def commit_mode_state(telegram_id: int, data: dict, session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            res = await session.stream(select(User).where(User.telegram_user_id == telegram_id))
            async for row in res.scalars():
                try:
                    row.training_mode_state.update(data)
                    flag_modified(row, "training_mode_state")
                    session.add(row)
                    # print(type(row.training_mode_state), row.training_mode_state)
                except Exception as ex:
                    return "Что то пошло не так, попробуйте еще раз."

            await session.commit()
            return "Тренировочный режим был включен"

async def fetch_mode_state(session_maker:sessionmaker):
    async with session_maker() as session:
        async with session.begin():
            res = await session.stream(select(User).where(User.training_mode_state != {}))
            all_active_mode_users_list = []
            async for row in res.scalars():
                all_active_mode_users_list.append({"user":row.telegram_user_id,"mode":row.training_mode_state})
            return all_active_mode_users_list