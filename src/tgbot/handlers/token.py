from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.states.token_state import Token


async def token_handler_init(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Token init")
    await bot.set_state(message.from_user.id, Token.end, message.chat.id)


async def token_handler_end(message: Message, bot: AsyncTeleBot):
    await bot.send_message(message.chat.id, "Token end")
    await bot.delete_state(message.from_user.id, message.chat.id)
