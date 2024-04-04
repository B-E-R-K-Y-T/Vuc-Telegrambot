from typing import Optional

from telebot.async_telebot import AsyncTeleBot

from logger import LOGGER
from tgbot.services.tasks.handler_collector import HandlersTaskCollector
from tgbot.services.tasks.types import TaskTypes, StatusTask

handlers_collector = HandlersTaskCollector()


@handlers_collector.add_handler(TaskTypes.SEND_USER_MESSAGE)
async def send_message_user(bot: AsyncTeleBot, telegram_id: int, message: str):
    message = await bot.send_message(telegram_id, message)

    return {
        "status_task": StatusTask.COMPLETED,
        "message_id": message.message_id,
        "chat_id": message.chat.id,
        "text": message.text
    }


@handlers_collector.add_handler(TaskTypes.SEND_PLATOON_MESSAGE)
async def send_message_users(bot: AsyncTeleBot, users_tg: list, message: str):
    result = []
    message_result: Optional[dict] = None

    for telegram_id in users_tg:
        try:
            msg = await bot.send_message(telegram_id, message)
            message_result = {
                "status_task": StatusTask.COMPLETED,
                "telegram_id": telegram_id,
                "message_id": msg.message_id,
                "chat_id": msg.chat.id,
                "text": msg.text
            }
        except Exception as e:
            LOGGER.error(str(e))
            message_result = {
                "status_task": StatusTask.ERROR,
                "telegram_id": telegram_id,
                "detail": str(e)
            }
        finally:
            result.append(message_result)

    return {
        "status_task": StatusTask.COMPLETED,
        "messages": result
    }
