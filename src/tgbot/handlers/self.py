from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.services.api_worker.client import APIWorker
from tgbot.services.user import UsersFactory
from tgbot.services.utils.message_tools import send_status_task_smile


@send_status_task_smile()
async def self(message: Message, bot: AsyncTeleBot):
    api = APIWorker()
    user = await UsersFactory().get_user(message)

    token = await user.token
    user_id = await user.user_id

    data = await api.get_self(token, user_id)
    format_data = "".join([f"* {k} = {v}\n" for k, v in data.items()])

    await bot.send_message(message.chat.id, f"{format_data}")
