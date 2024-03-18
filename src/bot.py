import asyncio

from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from config import app_settings
from exceptions import VucExceptionHandler
from tgbot.filters.admin_filter import AdminFilter
from tgbot.filters.check_login import CheckLogin
from tgbot.handlers.cancel import cancel_state
from tgbot.handlers.default_message import default_answer
from tgbot.handlers.login import (
    login_handler_init,
    login_handler_email,
    login_handler_password,
)
from tgbot.handlers.logout import logout_handler
from tgbot.handlers.menu.callback_handler import callback_handler
from tgbot.handlers.menu.inline_menu import menu_handler
from tgbot.handlers.menu.outline_menu import handle_outline_output
from tgbot.handlers.self import self
from tgbot.handlers.set_attend import set_attend
from tgbot.handlers.start import start_command_handler
from tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware
from tgbot.services.commands import CommandSequence
from tgbot.services.outline_text_buttons import OutlineKeyboardButton
from tgbot.services.utils.callback_data import CallBackData
from tgbot.states.login import Login
from tgbot.states.setter_states import *

bot = AsyncTeleBot(
    app_settings.TOKEN,
    state_storage=StateMemoryStorage(),
    exception_handler=VucExceptionHandler(),
)


def init_handlers():
    def init_base_filters(*args, callback_query_flag: bool = False, **kwargs):
        if not callback_query_flag:
            bot.register_message_handler(*args, **kwargs, check_login=True)
        else:
            bot.register_callback_query_handler(*args, **kwargs, check_login=True)

    bot.register_message_handler(
        start_command_handler, commands=[CommandSequence.START], pass_bot=True
    )

    bot.register_message_handler(
        handle_outline_output, func=lambda msg: msg.text in OutlineKeyboardButton.fields(), pass_bot=True
    )

    init_base_filters(self, commands=[CommandSequence.SELF], pass_bot=True)
    init_base_filters(logout_handler, commands=[CommandSequence.LOGOUT], pass_bot=True)
    init_base_filters(menu_handler, commands=[CommandSequence.MENU], pass_bot=True)

    init_base_filters(
        callback_handler,
        func=lambda call: True,
        callback_query_flag=True,
        pass_bot=True,
    )

    bot.register_message_handler(
        cancel_state, commands=[CommandSequence.CANCEL], pass_bot=True
    )
    bot.register_message_handler(
        login_handler_init, commands=[CommandSequence.LOGIN], pass_bot=True
    )

    bot.register_message_handler(login_handler_email, pass_bot=True, state=Login.email)
    bot.register_message_handler(
        login_handler_password, pass_bot=True, state=Login.password
    )

    init_base_filters(
        default_answer,
        pass_bot=True,
        func=lambda msg: msg.text not in CommandSequence.fields(),
    )


def init_middlewares():
    middlewares = (
        AntiFloodMiddleware(
            timeout=app_settings.TIMEOUT_MESSAGES,
            max_messages=app_settings.MAX_MESSAGES,
            interval=app_settings.INTERVAL,
            bot=bot,
        ),
    )

    for middleware in middlewares:
        bot.setup_middleware(middleware)


def init_filters():
    filters = (
        AdminFilter(),
        CheckLogin(bot),
        asyncio_filters.StateFilter(bot),
    )

    for filter_ in filters:
        bot.add_custom_filter(filter_)


async def run():
    await bot.polling(non_stop=True)


if __name__ == "__main__":
    init_handlers()
    init_middlewares()
    init_filters()

    asyncio.run(run())
