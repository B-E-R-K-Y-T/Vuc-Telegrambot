from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message

from tgbot.services.commands import CommandSequence
from tgbot.handlers.menu.outline_menu import create_start_outline_menu_handler


async def start_command_handler(message: Message, bot: AsyncTeleBot):
    markup = await create_start_outline_menu_handler()
    await bot.send_message(
        message.chat.id,
        f"Приветствую Вас.\n\n"
        f"Чтобы войти, используйте команду: /{CommandSequence.LOGIN}",
        reply_markup=markup
    )
