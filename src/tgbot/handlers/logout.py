from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.api_worker.client import APIWorker
from tgbot.user import UsersFactory
from tgbot.utils.message_tools import send_wait_smile


@send_wait_smile
async def logout_handler(message: Message, bot: AsyncTeleBot):
    api = APIWorker()
    user = await UsersFactory().get_user(message)

    if await api.logout(await user.token):
        await UsersFactory().delete_user(user.telegram_id)
        await bot.send_message(message.chat.id, "Вы вышли из аккаунта.")
    else:
        await bot.send_message(message.chat.id, "Ошибка.")
