from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.commands import CommandSequence


async def start_command_handler(message: Message, bot: AsyncTeleBot):
    await bot.send_message(
        message.chat.id,
        f"Приветствую Вас.\n\n"
        f"Чтобы войти, используйте команду: /{CommandSequence.LOGIN}",
    )
