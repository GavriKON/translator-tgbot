import asyncio
import logging
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from buttons import user_keyboard_onstart, user_keyboard_change_lang, add_to_dictionary_inline_keyboard, delete_from_dictionary_inline_key, confirmation_button
from handlers.general import inline_translater,take_user_timezone, text_to_speech
from db.commands import add_user, get_user,commit_dictionary, get_user_dictionary, delete_from_dictionary, clear_all_dictionary, take_all_users
from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from middlewares.register_check import RegisterCheck, set_key

@set_key('registerd')
async def command_start(message: types.Message):
    db_session = message.bot.get("db")

    #! await add_user(message.from_user.id, db_session)

    html_title = inline_translater(
        """Привет! Я - бот, который заставить тебя учить языки, как бы тебе не было лень.\n
<b>ТЕБЕ ПРИДЕТСЯ!</b>\n
📌Для того что бы сменить язык, используй команду /change_language.\n
📌Для того чтобы просмотреть свой словарь используй команду /dictionary.\n
✅В целом, все сделано легко и понятно, просто напиши слово на своем языке и я сразу переведу его на выбраный тобой язык!\n
<b>🔥Давайте учить языки!</b>""", (await get_user(message.from_user.id, db_session)).bot_language)

    await bot.send_message(message.from_user.id,
                           html_title,
                           reply_markup=user_keyboard_onstart,
                           parse_mode='HTML')

async def clear_dictionary_cmd(message: types.Message):
    db_session = message.bot.get("db")

    output_lang = (await get_user(message.from_user.id, db_session)).bot_language
    
    await message.reply(inline_translater(f"Вы уверены что хотите <b>ОЧИСТИТЬ</b> ваш словарь?", output_lang), reply_markup=confirmation_button, parse_mode='HTML')

@dp.callback_query_handler(Text(endswith='_clear_dict'))
async def clear_dictionary(callback: types.CallbackQuery):
    db_session = callback.bot.get("db")
    if callback.data.split('_')[0] == 'yes':
        try:
            await clear_all_dictionary(callback.from_user.id, db_session)
            output_lang = (await get_user(callback.from_user.id, db_session)).bot_language
            await callback.answer(inline_translater("The Dictionary has been cleared!", output_lang), show_alert=True)
        except Exception as ex:
            return ex
    elif callback.data.split('_')[0] == 'no':
        await callback.message.delete()
        
@set_key('registerd')           
async def view_dictionary_cmd(message: types.Message):
    db_session = message.bot.get("db")
    try:
        json_respons = await get_user_dictionary(message.from_user.id, db_session)
        # print(json_respons['dictionary'][0])
        output_lang = (await get_user(message.from_user.id, db_session)).bot_language
        if json_respons['dictionary']:
            if len(json_respons['dictionary']) > 0:
                for words in range(0, len(json_respons['dictionary'])):
                    msg_parse = await message.answer(f""" <b>{inline_translater('Word (Phrase)'.capitalize(), output_lang)}:</b> <code>{json_respons['dictionary'][words]["translation"]}</code>\n<b>{inline_translater('Translation', output_lang)}:</b> <code>{json_respons['dictionary'][words]["message"]}</code>
                    """, reply_markup=delete_from_dictionary_inline_key(words))
        else:
            await message.answer(inline_translater("Ваш словарь пуст, добавте в него пару новых слов!📝", output_lang))

    except Exception as ex:
        await message.answer("<b>You haven't registerd</b> yet.\nTo enable the bot type /start, or any word.", parse_mode='HTML')
        logging.exception(ex)

@dp.callback_query_handler(Text(endswith='delete'))
async def delete_word_from_dictionary(callback: types.CallbackQuery):
    db_session = callback.bot.get("db")

    output_lang = (await get_user(callback.from_user.id, db_session)).bot_language
    await callback.answer(inline_translater("The dictionary has been updated", output_lang), show_alert=True)
    await callback.message.delete()

    await delete_from_dictionary(callback.from_user.id, int(callback.data.split('_')[0]), db_session)


@set_key('registerd')
async def echo_send_translation(message: types.Message):
    global json_application

    db_session = message.bot.get("db")
    
    user = await get_user(message.from_user.id, db_session)

    result = inline_translater(message=message.text, lang=user.translation_language)

    json_application = {"message": str(message.text).capitalize(), "translation": str(result), 'notification_time': None}

    await message.reply(result, reply_markup=add_to_dictionary_inline_keyboard(json_application['translation']))


@dp.callback_query_handler(Text(equals='add'))
async def add_word_to_dictionary(callback: types.CallbackQuery):

    db_session = callback.bot.get("db")

    jsonb = json_application

    await commit_dictionary(callback.from_user.id, jsonb,db_session)

    output_lang = (await get_user(callback.from_user.id, db_session)).bot_language

    await callback.answer(inline_translater("The dictionary has been updated", output_lang))


@dp.callback_query_handler(Text(endswith='speech'))
async def send_audio(callback: types.CallbackQuery):

    translated = callback.data.split('_')[0]

    audio = text_to_speech(translated)

    audio_title = f"{translated[:15]}" if len(translated) <= 15 else f"{translated[:15]}..."

    await callback.bot.send_audio(callback.from_user.id, audio=audio, title=audio_title)

def register_handlers_client(dp: Dispatcher):
    dp.register_message_handler(
        command_start, Text(equals=['start', 'help'], ignore_case=True))
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(clear_dictionary_cmd, Text(equals="Clear Dictionary 🗑", ignore_case=True))
    dp.register_message_handler(clear_dictionary_cmd, commands='clear_dictionary')
    dp.register_message_handler(view_dictionary_cmd, Text(equals=['dictionary 📖','dictionary'], ignore_case=True))
    dp.register_message_handler(view_dictionary_cmd, commands='dictionary')
    dp.register_message_handler(echo_send_translation)