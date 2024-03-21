from typing import Optional

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.services.tasks.task_collector import HandlerTaskCollector
from tgbot.services.tasks.types import TaskTypes, StatusTask

handlers_collector = HandlerTaskCollector()


@handlers_collector.add_handler(TaskTypes.SEND_USER_MESSAGE)
async def send_message_user(bot: AsyncTeleBot, telegram_id: int, message: str) -> Optional[Message]:
    await bot.send_message(telegram_id, message)

    return StatusTask.FINISHED
