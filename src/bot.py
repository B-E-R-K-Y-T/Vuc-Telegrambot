import asyncio

from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot

from telebot.asyncio_storage import StateMemoryStorage

from tgbot.filters.admin_filter import AdminFilter
from tgbot.handlers.admin import admin_user
from tgbot.handlers.default_message import default_answer
from tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware
from config import app_settings

bot = AsyncTeleBot(app_settings.TOKEN, state_storage=StateMemoryStorage())


def register_handlers():
    bot.register_message_handler(
        admin_user, commands=["start"], admin=True, pass_bot=True
    )
    bot.register_message_handler(default_answer, pass_bot=True)


async def run():
    await bot.polling(non_stop=True)


if __name__ == '__main__':
    register_handlers()

    bot.add_custom_filter(AdminFilter())
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))

    # Middlewares
    bot.setup_middleware(
        AntiFloodMiddleware(
            timeout=app_settings.TIMEOUT_MESSAGES,
            max_messages=app_settings.MAX_MESSAGES,
            bot=bot
        )
    )

    asyncio.run(run())
