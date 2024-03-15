from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.api_worker.client import APIWorker
from tgbot.user import User
from tgbot.utils.message_tools import send_wait_smile


@send_wait_smile
async def self(message: Message, bot: AsyncTeleBot):
    api = APIWorker()
    user = await User(message.from_user.id).ainit()

    token = user.token
    user_id = user.user_id

    data = await api.get_self(token, user_id)
    format_data = ''.join([f"* {k} = {v}\n" for k, v in data.items()])

    await bot.send_message(message.chat.id, f"{format_data}")
