from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from exceptions import BackgroundTaskError
from tgbot.services.api_worker.client import APIWorker
from tgbot.services.user import UsersFactory
from tgbot.services.utils.message_tools import send_status_task_smile


@send_status_task_smile()
async def logout_handler(message: Message, bot: AsyncTeleBot):
    api = APIWorker()
    user = await UsersFactory().get_user(message)

    if await api.logout(await user.token):
        await UsersFactory().delete_user(user.telegram_id)
    else:
        raise BackgroundTaskError
