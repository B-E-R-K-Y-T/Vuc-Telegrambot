import asyncio

from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from tgbot.commands import CommandSequence
from tgbot.filters.admin_filter import AdminFilter
from tgbot.filters.check_login import CheckLogin
from tgbot.handlers.cancel import cancel_state
from tgbot.handlers.default_message import default_answer
from exceptions import VucExceptionHandler
from tgbot.handlers.login import (
    login_handler_init,
    login_handler_email,
    login_handler_password,
)
from tgbot.handlers.logout import logout_handler
from tgbot.handlers.menu import menu_handler, student_menu, back, platoon_menu, squad_menu, marks_menu, attend_menu, \
    personal_menu
from tgbot.handlers.self import self
from tgbot.handlers.setters_pd import set_name, init_name_state
from tgbot.handlers.start import start_command_handler
from tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware
from config import app_settings
from tgbot.states.login import Login
from tgbot.states.set_name import SetName
from tgbot.utils.callback_data import CallBackData

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
    init_base_filters(
        self, commands=[CommandSequence.SELF], pass_bot=True
    )
    init_base_filters(logout_handler, commands=[CommandSequence.LOGOUT], pass_bot=True)
    init_base_filters(menu_handler, commands=[CommandSequence.MENU], pass_bot=True)

    init_base_filters(
        student_menu,
        func=lambda call: call.data == CallBackData.STUDENT_MENU,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        squad_menu,
        func=lambda call: call.data == CallBackData.SQUAD_MENU,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        platoon_menu,
        func=lambda call: call.data == CallBackData.PLATOON_MENU,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        marks_menu,
        func=lambda call: call.data == CallBackData.MARK,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        attend_menu,
        func=lambda call: call.data == CallBackData.ATTEND,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        personal_menu,
        func=lambda call: call.data == CallBackData.PERSONAL_DATA,
        callback_query_flag=True,
        pass_bot=True,
    )

    init_base_filters(
        init_name_state,
        func=lambda call: call.data == CallBackData.NAME,
        callback_query_flag=True,
        pass_bot=True,
    )

    init_base_filters(
        back,
        func=lambda call: call.data == CallBackData.BACK,
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
        set_name, pass_bot=True, state=SetName.init
    )

    init_base_filters(
        default_answer,
        pass_bot=True,
        func=lambda msg: msg.text not in CommandSequence.commands(),
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
