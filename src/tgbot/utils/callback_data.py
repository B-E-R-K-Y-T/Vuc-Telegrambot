import asyncio
from copy import copy
from functools import wraps
from typing import Callable

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery


class _auto_callback_data:
    state = 0

    def __new__(cls, *args, **kwargs):
        cls.state += 1

        return str(cls.state)


class CallBackStackWorker:
    def __init__(self):
        self.__stack: dict[int, list[dict[Callable, tuple]]] = {}
        self.__root: dict = {}

    def get_root_id(self, chat_id: int) -> int | None:
        return self.__root.get(chat_id)

    def set_root_id(self, chat_id: int, metadata: Message | CallbackQuery) -> None:
        self.__root[chat_id] = self.__get_message_id(metadata)

    def add_call(
        self,
        chat_id: int,
        func: Callable,
        bot: AsyncTeleBot,
        metadata: Message | CallbackQuery,
        message_id,
        is_root: bool = False
    ):
        if self.__stack.get(chat_id) is None:
            self.__stack[chat_id] = []

        self.__stack[chat_id].append({func: (metadata, bot, message_id, is_root)})

    def get_last_call(self, chat_id: int) -> dict:
        if self.__stack.get(chat_id) is not None:
            if len(self.__stack[chat_id]) >= 2:
                call = copy(self.__stack[chat_id][-2])
                self.__stack[chat_id].pop(-1)
                return call

    def listen_call(self, is_root: bool = False):
        def decorator(func):
            @wraps(func)
            async def wrapper(
                metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs
            ) -> Callable:
                if isinstance(metadata, Message):
                    chat_id = metadata.chat.id
                    message_id = metadata.message_id
                elif isinstance(metadata, CallbackQuery):
                    chat_id = metadata.message.chat.id
                    message_id = metadata.message.message_id
                else:
                    raise TypeError

                self.add_call(
                    chat_id,
                    func,
                    bot,
                    metadata,
                    message_id,
                    is_root=is_root
                )

                if asyncio.iscoroutinefunction(func):
                    return await func(metadata, bot, *args, **kwargs)
                else:
                    return func(metadata, bot, *args, **kwargs)

            return wrapper

        return decorator

    @staticmethod
    def __get_message_id(metadata: Message | CallbackQuery):
        if isinstance(metadata, Message):
            return metadata.message_id
        elif isinstance(metadata, CallbackQuery):
            return metadata.message.message_id
        else:
            raise TypeError

    def __repr__(self):
        return f"<{self.__class__.__name__}> STACK: {self.__stack}"


class CallBackData:
    MARK = _auto_callback_data()
    ATTEND = _auto_callback_data()
    PERSONAL_DATA = _auto_callback_data()

    SEMESTER_ONE = _auto_callback_data()
    SEMESTER_TWO = _auto_callback_data()
    SEMESTER_THREE = _auto_callback_data()
    SEMESTER_FOUR = _auto_callback_data()
    SEMESTER_FIVE = _auto_callback_data()
    SEMESTER_SIX = _auto_callback_data()

    STUDENT_MENU = _auto_callback_data()
    SQUAD_MENU = _auto_callback_data()
    PLATOON_MENU = _auto_callback_data()

    ADD_STUDENT = _auto_callback_data()
    MOVE_STUDENT = _auto_callback_data()

    NAME = _auto_callback_data()
    DOB = _auto_callback_data()
    PHONE = _auto_callback_data()
    EMAIL = _auto_callback_data()
    ADDRESS = _auto_callback_data()
    INSTITUTE = _auto_callback_data()
    DOS = _auto_callback_data()
    GROUP_STUDY = _auto_callback_data()
    PLATOON_NUMBER = _auto_callback_data()
    SQUAD_NUMBER = _auto_callback_data()
    ROLE = _auto_callback_data()
    TELEGRAM_ID = _auto_callback_data()

    BACK = _auto_callback_data()


__all__ = (
    CallBackData.__name__,
)
