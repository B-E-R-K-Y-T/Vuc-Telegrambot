from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message


async def cancel_state(message: Message, bot: AsyncTeleBot):
    """
    Cancel state
    """
    await bot.send_message(message.chat.id, 'Отмена.')
    await bot.delete_state(message.from_user.id, message.chat.id)
