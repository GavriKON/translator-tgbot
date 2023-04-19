from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from aiogram import types, Dispatcher
from create_bot import dp, bot
from buttons import bot_lang_buttons_kbrd, change_trans_lang_buttons,user_keyboard_change_lang,user_keyboard_onstart
from handlers.general import inline_translater
from db.commands import commit_bot_language,get_user, commit_translation_language

emoji_dict = {'eng':"🇬🇧",'fr':"🇫🇷",'de':'🇩🇪','uk':"🇺🇦",'ru':"🇷🇺", 'ita':"🇮🇹"}

to = ['eng','fr','de','uk','ru','ita']

class FSMAdmin(StatesGroup):
    lang_options = State()
    language = State()

bot_state_list = lambda x: any(word in x for word in ["Bot", "bot"])
        
translate_state_list = lambda x: any(word in x for word in ["translation", "Translation","translate"])

        
async def change_language(message: types.Message):
    await FSMAdmin.lang_options.set()
    await message.answer("Choose an option:",reply_markup=user_keyboard_change_lang)

async def load_options(message: types.Message, state: FSMContext):
    async with state.proxy() as data:
        data['lang_options'] = message.text
    await FSMAdmin.next()
    db_session = message.bot.get("db")
    if any(word in message.text for word in ["Bot", "bot"]):
        current_bot_lang = (await get_user(message.from_user.id, db_session)).bot_language
        await message.answer(f'Click on the desired language.\n<b>Now: {current_bot_lang.upper()} {emoji_dict.get(current_bot_lang)}</b>',
                       reply_markup=bot_lang_buttons_kbrd,
                       parse_mode='HTML')

    elif any(word in message.text for word in ["translation", "Translation","translate"]):
        current_lang = (await get_user(message.from_user.id, db_session)).translation_language
        await message.answer(f'Click on the desired translation language.\n<b>Now: {current_lang.upper()} {emoji_dict.get(current_lang)}</b>',
                       reply_markup=change_trans_lang_buttons,
                       parse_mode='HTML')


@dp.callback_query_handler(lambda call_back: call_back.data in to, state=FSMAdmin.language)
async def set_language(callback: types.CallbackQuery, state: FSMContext):
    async with state.proxy() as data:
        try:
            if bot_state_list(data['lang_options']):
                db_session = callback.bot.get("db")
                data['language'] = callback.data
                await commit_bot_language(callback.from_user.id, callback.data, db_session)
                await callback.message.delete()
                await callback.message.answer(inline_translater(
                    """Привет! Я - бот, который заставить тебя учить языки, как бы тебе не было лень.\n
            <b>ТЕБЕ ПРИДЕТСЯ!</b>\n
            📌Для того что бы сменить язык, используй команду /change_language.\n
            📌Для того чтобы просмотреть свой словарь используй команду /dictionary.\n
            ✅В целом, все сделано легко и понятно, просто напиши слово на своем языке и я сразу переведу его на выбраный тобой язык!\n
            <b>🔥Вперед учить языки!</b>""", callback.data),parse_mode='HTML',reply_markup=user_keyboard_onstart)
                
                await callback.answer(text=inline_translater(f"You switched bot language on {callback.data}", callback.data))
                await state.finish()

            elif translate_state_list(data['lang_options']):
                db_session = callback.bot.get("db")
                data['language'] = callback.data
                await commit_translation_language(callback.from_user.id, callback.data, db_session)
                user_current_bot_language = (await get_user(callback.from_user.id, db_session)).bot_language
                await callback.answer(text=inline_translater(f"You switched translation language on {(callback.data).upper()}", user_current_bot_language))
                await callback.message.delete()
                await callback.message.answer(text=f'<b>Current language:</b> <i>{callback.data.upper() + emoji_dict.get(callback.data)}</i> ',reply_markup=user_keyboard_onstart,parse_mode='HTML')
                await state.finish()
            # !!! QUESTION
        except:
            # callback: types.Message
            await callback.delete()
            user_language = (await get_user(callback.from_user.id, bot.get('db'))).bot_language
            await callback.answer(inline_translater("❗️SOMETHING WENT WRONG, TRY AGAIN!❗️", user_language), reply_markup=user_keyboard_onstart)
            await state.finish()


async def cancel_cmd(message: types.Message, state: FSMContext):
    current_state = await state.get_state()
    if current_state is None:
        return
    await state.finish()
    await message.reply("Canceled", reply_markup=user_keyboard_onstart)
        

def register_handlers_fsm(dp: Dispatcher):
    dp.register_message_handler(change_language, commands=['change_language'], state=None)
    dp.register_message_handler(change_language, Text(equals='Change language', ignore_case=True),state=None)
    dp.register_message_handler(load_options, Text(equals=["Bot Language", "Translation Language"], ignore_case=True), state=FSMAdmin.lang_options)
    dp.register_message_handler(set_language, state=FSMAdmin.language)
    dp.register_message_handler(cancel_cmd, commands=['cancel'], state="*")
    dp.register_message_handler(cancel_cmd, Text(equals='Cancel', ignore_case=True), state="*")