from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


async def default_answer(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Я Вас не понимаю.")
