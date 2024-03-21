from typing import Callable

from logger import LOGGER
from tgbot.services.tasks.types import StatusTask
from tgbot.services.utils.util import sync_async_call


class HandlerTaskCollector:
    __runner = None

    def __init__(self):
        self.__handlers: dict = {}

    def add_handler(self, name_type_task: str):
        def decorator(func: Callable):
            self.__handlers[name_type_task] = func

            return func

        return decorator

    @classmethod
    def add_runner(cls, runner):
        cls.__runner = runner

    async def start(self, name_type_task: str, **kwargs) -> StatusTask:
        func: Callable = self.__handlers.get(name_type_task)

        if not callable(func):
            raise TypeError

        try:
            return await sync_async_call(func, self.__runner, **kwargs)
        except Exception as e:
            LOGGER.error(str(e))
            return StatusTask.ERROR
