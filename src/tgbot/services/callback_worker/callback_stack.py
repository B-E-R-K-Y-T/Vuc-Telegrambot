from copy import copy
from functools import wraps
from typing import Callable, Awaitable, Optional, Any, Coroutine

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery

from exceptions import FunctionStackEmpty, StackRoot
from tgbot.services.utils.message_tools import get_message
from tgbot.services.utils.util import sync_async_call


class CallFunctionStack:
    def __init__(self):
        self.__stack = {}

    def get_last_function_image(self, chat_id: int, message_id: int) -> Optional[tuple]:
        if chat_id not in self.__stack:
            return None

        if message_id not in self.__stack[chat_id]:
            return None

        if len(self.__stack[chat_id][message_id]) == 1:
            return None

        function_image = copy(self.__stack[chat_id][message_id][-2])
        self.__stack[chat_id][message_id].pop(-1)

        return function_image

    def add(
            self,
            func: Callable | Awaitable,
            metadata: Message | CallbackQuery,
            bot: AsyncTeleBot,
            args,
            kwargs
    ):
        message: Message = get_message(metadata)
        chat_id: int = message.chat.id
        message_id = message.message_id

        if chat_id not in self.__stack:
            self.__stack[chat_id]: dict = {}

        if message_id not in self.__stack[chat_id]:
            self.__stack[chat_id][message_id]: list = []

        if not args and not kwargs:
            self.__stack[chat_id][message_id].append((func, metadata, bot))
        elif not args:
            self.__stack[chat_id][message_id].append((func, metadata, bot, kwargs))
        elif not kwargs:
            self.__stack[chat_id][message_id].append((func, metadata, bot, args))
        else:
            self.__stack[chat_id][message_id].append((func, metadata, bot, args, kwargs))

    def clear_message_stack(self, chat_id: int, message_id: int):
        if chat_id not in self.__stack:
            return None

        if message_id not in self.__stack[chat_id]:
            return None

        self.__stack[chat_id][message_id].clear()
        del self.__stack[chat_id][message_id]

    def get_stack(self):
        return self.__stack


class CallbackStackBuilder:
    def __init__(self, stack: CallFunctionStack):
        self.__stack = stack

    def root(self, func: Callable | Awaitable) -> Callable[
        [Message | CallbackQuery, AsyncTeleBot, tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs):
            message: Message = get_message(metadata)

            self.__stack.clear_message_stack(message.chat.id, message.message_id)

            result_metadata = await sync_async_call(func, metadata, bot, *args, **kwargs)

            self.__stack.add(func, result_metadata, bot, args, kwargs)

        return wrapper

    def listen_call(self, func: Callable | Awaitable) -> Callable[
        [Message | CallbackQuery, AsyncTeleBot, tuple[Any, ...], dict[str, Any]], Coroutine[Any, Any, Any]]:
        @wraps(func)
        async def wrapper(metadata: Message | CallbackQuery, bot: AsyncTeleBot, *args, **kwargs):
            self.__stack.add(func, metadata, bot, args, kwargs)

            return await sync_async_call(func, metadata, bot, *args, **kwargs)

        return wrapper


class StackStrider:
    def __init__(self, stack: CallFunctionStack, collector: CallbackStackBuilder):
        self.__stack = stack
        self.__collector = collector

    async def back(self, chat_id: int, message_id: int):
        function_image: Optional[tuple] = self.__stack.get_last_function_image(chat_id, message_id)

        if function_image is not None:
            func, _, _, _, _ = self.unpack_func_image(function_image)
            self.__collector.listen_call(func)

        if function_image is None:
            raise FunctionStackEmpty

        func, metadata, bot, args, kwargs = self.unpack_func_image(function_image)
        result_metadata = await sync_async_call(func, metadata, bot, *args, **kwargs)

        if len(self.__stack.get_stack()[chat_id][message_id]) == 1:
            func, _, bot, args, kwargs = self.unpack_func_image(function_image)
            self.__stack.clear_message_stack(chat_id, message_id)
            self.__stack.add(func, result_metadata, bot, args, kwargs)

            raise StackRoot

    @staticmethod
    def unpack_func_image(function_image: tuple) -> tuple:
        if len(function_image) == 3:
            return *function_image, (), {}
        elif len(function_image) == 4 and isinstance(function_image[3], tuple):
            return *function_image, {}
        elif len(function_image) == 4 and isinstance(function_image[3], dict):
            return *function_image, ()
        elif len(function_image) == 5:
            return function_image
