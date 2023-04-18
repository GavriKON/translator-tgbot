import asyncio
import logging
import datetime
import pytz
from quantumrandom import randint
from handlers.general import inline_translater
from aiogram.utils import executor
from middlewares.register_check import RegisterCheck
from create_bot import dp, bot, async_engine
from sqlalchemy.engine import URL
from sqlalchemy import exc
from db.commands import fetch_mode_state, get_user_dictionary, get_user
from db.User import User
from updatesworker import get_handled_updates_list

async def starter_sheduling():
    while True:
        try:
            fetch_res = await fetch_mode_state(bot.get('db'))
            for res in fetch_res:
                if res['mode']['IsActive']:
                    find_zone = pytz.timezone(res['mode']['timeInZone']) 
                    time_in_zone = datetime.datetime.now(find_zone)
                    currentTimeInZone = time_in_zone.strftime("%H:%M")

                    if currentTimeInZone == res['mode']['settedTimeByUser']:
                        
                        user_cell = await get_user_dictionary(res['user'],bot.get('db'))

                        if len(user_cell['dictionary']) > 0:
                            user_language = (await get_user(res['user'], bot.get('db'))).bot_language
                            gen_random_word_index = int(randint(0, len(user_cell['dictionary'])))
                            msg_parse = f"""<b>{inline_translater('Word (Phrase)'.capitalize(), user_language)}:</b> <code>{user_cell['dictionary'][gen_random_word_index]["translation"]}</code>\n<b>{inline_translater('Translation', user_language)}:</b> <code>{user_cell['dictionary'][gen_random_word_index]["message"]}</code>"""
                            await bot.send_message(res['user'], msg_parse, parse_mode='HTML')
                        else:
                            user_language = (await get_user(res['user'], bot.get('db'))).bot_language
                            await bot.send_message(inline_translater("Ваш словарь пуст, добавте в него пару новых слов!📝", user_language))
        except exc.SQLAlchemyError as ex:
            logging.exception(ex)

        await asyncio.sleep(60)

async def main():
    logging.basicConfig(level=logging.INFO)
    print("Bot is now polling")
    # postgres_url = URL.create(
    #     "postgresql+asyncpg",
    #     username="username",
    #     password="password",
    #     host="localhost",
    #     db_name = "dbname",
    #     port = "5432"
    # )
    from handlers import fsm, active_learning_fsm, users, general

    fsm.register_handlers_fsm(dp)
    active_learning_fsm.register_handlers_active_mode_fsm(dp)
    users.register_handlers_client(dp)

    try:
        dp.middleware.setup(RegisterCheck())
        await dp.start_polling(dp, allowed_updates=get_handled_updates_list(dp))
        
    finally:
        print("Bot is now stoped!")
        await dp.storage.close()
        await dp.storage.wait_closed()
        await bot.session.close()

if __name__ == '__main__':

    try:
        async def concurrency_main():
            await asyncio.gather(main(), starter_sheduling())
        asyncio.run(concurrency_main())

    except (KeyboardInterrupt, SystemExit):

        logging.error("Bot stopped!")
        