from typing import Callable, Dict, Any, Awaitable, Union

from aiogram.dispatcher.middlewares import BaseMiddleware
from aiogram.dispatcher.handler import CancelHandler, current_handler
from aiogram.types import Message, CallbackQuery


from db.commands import get_user,add_user, is_user_exists, alocate_dictionary


def set_key(key:str = None):

    def decorator(func):
        setattr(func, 'key', key)

        return func

    return decorator

class RegisterCheck(BaseMiddleware):
    """
    Middleware будет вызываться каждый раз, когда пользователь будет отправлять боту сообщения (или нажимать
    на кнопку в инлайн-клавиатуре).
    """

    async def on_process_message(
        self,
        message: Union[Message, CallbackQuery],
        data: dict
    ) -> Any:

        handler = current_handler.get()
        
        if handler:
            key = getattr(handler, "key", "No Atributte")

        session_maker = message.bot.get('db')
        redis = message.bot.get('redis')
        user = message.from_user
        # Получаем менеджер сессий из ключевых аргументов, переданных в start_polling()
        if not await is_user_exists(telegram_id=message.from_user.id, session_maker=session_maker, redis=redis):
            try:
                await add_user(telegram_id=message.from_user.id, session_maker=session_maker)
                await alocate_dictionary(telegram_id=message.from_user.id, session_maker=session_maker)
            except Exception:
                return

        else:
            print(f"User {user} have already reged!")
