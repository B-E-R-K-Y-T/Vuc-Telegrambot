from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.states.token_state import Token


async def start_command_handler(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, 'Введите Ваш токен: ')
    await bot.set_state(message.from_user.id, Token.init, message.chat.id)
