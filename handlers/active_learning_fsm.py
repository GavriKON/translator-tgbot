import time
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from buttons import user_keyboard_set_time, user_keyboard_onstart
from handlers.general import inline_translater, take_user_timezone
from db.commands import get_user, commit_mode_state, fetch_mode_state
from datetime import datetime

class FSMAdmin(StatesGroup):
    user_time = State()
    receiv_msg_time = State()


async def set_user_time(message: types.Message):
    global user_language
    db_session = message.bot.get("db")
    user_language = (await get_user(message.from_user.id, db_session)).bot_language
    set_user_time_text_help = inline_translater("🕓Пожалуйста, укажите ваше точное время прямо сейчас (<b>ПРИМЕР:</b> <i>12:36</i>)",user_language)
    await FSMAdmin.user_time.set()
    await message.answer(set_user_time_text_help, parse_mode='HTML', reply_markup=user_keyboard_set_time)

async def set_reacive_msg_time(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            validate_time = time.strptime(message.text, '%H:%M')
            data['user_time'] = message.text
            await FSMAdmin.next()
            await message.answer(inline_translater("✏️Напишите время в которое хотите получать <b>сообщения</b> (ПРИМЕР: 14:00)", user_language), parse_mode='HTML')
        except ValueError:
            await set_user_time(message)

async def commit_active_mode(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        try:
            validate_time = time.strptime(message.text, '%H:%M')
            data['receiv_msg_time'] = str(message.text)
        except:
            await message.answer(inline_translater("✏️Напишите время в которое хотите получать <b>сообщения</b> (ПРИМЕР: 14:00)", user_language), parse_mode='HTML')
            return await state.set_state(FSMAdmin.receiv_msg_time)

    db_session = message.bot.get("db")
    
    user_time = data['user_time']
    recieve_msg_time = datetime.strptime(str(data['receiv_msg_time']), '%H:%M').time()
    
    res = take_user_timezone(user_time, recieve_msg_time)

    answer_in_chat = await commit_mode_state(message.from_user.id, res, db_session)
    await message.answer(inline_translater(answer_in_chat, user_language), parse_mode='HTML', reply_markup=user_keyboard_onstart)
    await state.finish()
    
async def cancel_cmd(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Canceled", reply_markup=user_keyboard_onstart)

def register_handlers_active_mode_fsm(dp: Dispatcher):
    dp.register_message_handler(set_user_time, commands=['training_mode'], state=None)
    dp.register_message_handler(set_user_time, Text(equals=['Active Learning 📆','Active Learning']),state=None)
    dp.register_message_handler(set_reacive_msg_time, state=FSMAdmin.user_time)
    dp.register_message_handler(commit_active_mode, state=FSMAdmin.receiv_msg_time)
    dp.register_message_handler(cancel_cmd, commands=['cancel'], state="*")
    dp.register_message_handler(cancel_cmd, Text(equals='Cancel', ignore_case=True), state="*")