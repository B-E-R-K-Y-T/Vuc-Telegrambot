from functools import wraps
from typing import Callable

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.api_worker.client import APIWorker
from tgbot.user import User


def init_user_id(coro: Callable) -> Callable:
    @wraps(coro)
    async def wrapper(self, *args, **kwargs):
        user_id = await self.api.get_user_id(await self.user.get_jwt(), self.tg_id)

        return await coro(self, *args, user_id, **kwargs)

    return wrapper


class Student:
    def __init__(self, tg_id: int):
        self.api = APIWorker()
        self.tg_id = tg_id
        self.user = User(tg_id)

    @init_user_id
    async def marks(self, user_id):
        print(user_id)
        semesters = [1, 2, 3]
        keyboard = InlineKeyboardMarkup(row_width=7)

        for semester in semesters:
            keyboard.add(
                InlineKeyboardButton(
                    text=f'Semester {semester}',
                    callback_data='2'
                )
            )
