from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton


help_button = KeyboardButton('Help')

dictionary_button = KeyboardButton('Dictionary 📖')

change_lang_button = KeyboardButton('Change language')

clear_all_dict = KeyboardButton("Clear Dictionary 🗑")

active_learning_button = KeyboardButton("Active Learning 📆")

user_keyboard_onstart = ReplyKeyboardMarkup(resize_keyboard=True)

user_keyboard_onstart.add(change_lang_button).insert(dictionary_button).add(clear_all_dict).insert(active_learning_button).add(
    help_button)

###?CHANGE LANGUAGES INLINE KEYBOARD?###

change_bot_lang_btn = KeyboardButton("Bot Language")

change_trans_lang_btn = KeyboardButton("Translation Language")

cancel_lang_btn = KeyboardButton("Cancel")

user_keyboard_change_lang = ReplyKeyboardMarkup(resize_keyboard=True)

user_keyboard_change_lang.add(change_bot_lang_btn).insert(
    change_trans_lang_btn).add(cancel_lang_btn)

###?!CHOOSE LANGUAGES INLINE BUTTONS?!###

bot_lang_buttons_kbrd = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="RU 🇷🇺", callback_data='ru')).add(InlineKeyboardButton(text='ENG 🇬🇧', callback_data='eng')).add(InlineKeyboardButton(text='UKR 🇺🇦', callback_data='uk')).add(InlineKeyboardButton(text='DE 🇩🇪', callback_data='de'))


change_trans_lang_buttons = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text="Русский 🇷🇺", callback_data='ru')).add(InlineKeyboardButton(text='English 🇬🇧', callback_data='eng')).add(InlineKeyboardButton(text='Український 🇺🇦', callback_data='uk')).add(InlineKeyboardButton(text='Deutsch 🇩🇪', callback_data='de')).add(InlineKeyboardButton(text='Français 🇫🇷', callback_data='fr')).add(InlineKeyboardButton(text='Italiano 🇮🇹', callback_data='ita'))

###? Add to dictionary inline button ?###
# dict_implementation = CallbackData('add','action', 'message')
add_to_dictionary_inline_key = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Add to dictionary ➕", callback_data="add"))

###? Delete from dictionary inline button ?###
def delete_from_dictionary_inline_key(word_id:int):
    delete_from_dictionary_inline_keyboard = InlineKeyboardMarkup(row_width=1).add(InlineKeyboardButton(text="Delete from dictionary ❌", callback_data=f"{word_id}_delete"))
    return delete_from_dictionary_inline_keyboard

###? Clear Dictionary buttons ?###

confirmation_button = InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(text='Yes ✅',callback_data='yes_clear_dict')).add(InlineKeyboardButton(text='No ❌',callback_data='no_clear_dict'))

###? ACTIVE LEARNING MODE KEYBOARD ?###

disable_training_mode = KeyboardButton("Disable 'Active Learning' ❌")

cancel_settings = KeyboardButton("Cancel")

user_keyboard_set_time = ReplyKeyboardMarkup(resize_keyboard=True)

user_keyboard_set_time.add(disable_training_mode).add(
    cancel_settings)

