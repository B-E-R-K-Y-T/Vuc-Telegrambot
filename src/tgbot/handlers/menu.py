from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


async def menu_handler(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, 'MENU')
