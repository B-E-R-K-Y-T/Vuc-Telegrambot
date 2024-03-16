from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.services.commands import CommandSequence


async def default_answer(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id,
        f"Я Вас не понимаю.\n\n"
        f"Попробуйте использовать команду: /{CommandSequence.MENU}",
    )
