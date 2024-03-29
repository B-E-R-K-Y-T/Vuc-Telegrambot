import asyncio

from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot

from telebot.asyncio_storage import StateMemoryStorage

from tgbot.commands import Command
from tgbot.filters.admin_filter import AdminFilter
from tgbot.handlers.cancel import cancel_state
from tgbot.handlers.default_message import default_answer
from exceptions import VucExceptionHandler
from tgbot.handlers.login import login_handler_init, login_handler_email, login_handler_password
from tgbot.handlers.start import start_command_handler
from tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware
from config import app_settings
from tgbot.states.login import Login

bot = AsyncTeleBot(app_settings.TOKEN, state_storage=StateMemoryStorage(), exception_handler=VucExceptionHandler())


def init_handlers():
    bot.register_message_handler(
        start_command_handler, commands=[Command.START], pass_bot=True
    )
    bot.register_message_handler(
        cancel_state, commands=[Command.CANCEL], pass_bot=True
    )
    bot.register_message_handler(
        login_handler_init, commands=[Command.LOGIN], pass_bot=True
    )

    bot.register_message_handler(
        login_handler_email, pass_bot=True, state=Login.email
    )
    bot.register_message_handler(
        login_handler_password, pass_bot=True, state=Login.password
    )

    bot.register_message_handler(default_answer, pass_bot=True)


async def run():
    await bot.polling(non_stop=True)


if __name__ == "__main__":
    init_handlers()

    bot.add_custom_filter(AdminFilter())
    bot.add_custom_filter(asyncio_filters.StateFilter(bot))

    # Middlewares
    bot.setup_middleware(
        AntiFloodMiddleware(
            timeout=app_settings.TIMEOUT_MESSAGES,
            max_messages=app_settings.MAX_MESSAGES,
            interval=app_settings.INTERVAL,
            bot=bot,
        )
    )

    asyncio.run(run())
