from typing import Callable, Awaitable, Optional

from logger import LOGGER
from tgbot.services.tasks.types import StatusTask
from tgbot.services.utils.util import sync_async_call

from telebot.async_telebot import AsyncTeleBot


class HandlersTaskCollector:
    __runner: Optional[AsyncTeleBot] = None

    def __init__(self):
        self.__handlers: dict = {}

    def add_handler(self, name_type_task: str) -> Callable:
        def decorator(func: Callable | Awaitable) -> Callable | Awaitable:
            self.__handlers[name_type_task] = func

            return func

        return decorator

    @classmethod
    def add_runner(cls, runner):
        cls.__runner = runner

    async def start(self, name_type_task: str, **kwargs) -> dict:
        func: Callable | Awaitable = self.__handlers.get(name_type_task)

        if not callable(func):
            raise TypeError

        try:
            return await sync_async_call(func, self.__runner, **kwargs)
        except Exception as e:
            LOGGER.error(str(e))
            return {"status_task": StatusTask.ERROR, "detail": str(e)}
