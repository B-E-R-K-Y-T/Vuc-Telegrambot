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
from tgbot.handlers.help import cmd_help
from tgbot.handlers.login import (
    login_handler_init,
    login_handler_email,
    login_handler_password,
)
from tgbot.handlers.set_attend import set_positive_attend, set_negative_attend
from tgbot.handlers.setters_pd import (
    set_dos,
    set_phone,
    set_address,
    set_institute,
    set_dob,
    set_group_study,
    set_name,
    set_email,
)
from tgbot.handlers.logout import logout_handler
from tgbot.services.callback_worker.callback_handler import callback_handler
from tgbot.handlers.menu.inline_menu import menu_handler
from tgbot.handlers.menu.outline_menu import handle_outline_output
from tgbot.handlers.self import personal_info
from tgbot.handlers.start import start_command_handler
from tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware
from tgbot.services.commands import CommandSequence
from tgbot.services.outline_text_buttons import OutlineKeyboardButton
from tgbot.services.tasks.handler_collector import HandlersTaskCollector
from tgbot.services.tasks.worker import task_server
from tgbot.states.attend import PositiveAttend, NegativeAttend
from tgbot.states.login import Login
from tgbot.states.setter_states import SetName, SetDob, SetGroupStudy, SetPhone, SetAddress, SetEmail, SetDos, \
    SetInstitute

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
        cmd_help, commands=[CommandSequence.HELP], pass_bot=True
    )

    bot.register_message_handler(
        handle_outline_output, func=lambda msg: msg.text in OutlineKeyboardButton.fields(), pass_bot=True
    )

    init_base_filters(personal_info, commands=[CommandSequence.SELF], pass_bot=True)
    init_base_filters(logout_handler, commands=[CommandSequence.LOGOUT], pass_bot=True)
    init_base_filters(menu_handler, commands=[CommandSequence.MENU], pass_bot=True)

    init_base_filters(
        callback_handler,
        func=lambda call: True,
        callback_query_flag=True,
        pass_bot=True,
    )

    # ---Сеттеры персональных данных------------------------------------------------------------------------------------
    # setters_pd = {
    #     set_name: SetName.init,
    #     set_dob: SetName.init,
    #     set_name: SetName.init,
    # }
    #
    init_base_filters(set_name, pass_bot=True, state=SetName.init)
    init_base_filters(set_dob, pass_bot=True, state=SetDob.init)
    init_base_filters(set_group_study, pass_bot=True, state=SetGroupStudy.init)
    init_base_filters(set_phone, pass_bot=True, state=SetPhone.init)
    init_base_filters(set_address, pass_bot=True, state=SetAddress.init)
    init_base_filters(set_email, pass_bot=True, state=SetEmail.init)
    init_base_filters(set_dos, pass_bot=True, state=SetDos.init)
    init_base_filters(set_institute, pass_bot=True, state=SetInstitute.init)
    # ------------------------------------------------------------------------------------------------------------------

    init_base_filters(set_positive_attend, pass_bot=True, state=PositiveAttend.init)
    init_base_filters(set_negative_attend, pass_bot=True, state=NegativeAttend.init)

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


async def bot_task():
    await bot.polling(non_stop=True)


async def main():
    init_handlers()
    init_middlewares()
    init_filters()

    HandlersTaskCollector.add_runner(bot)

    await asyncio.gather(bot_task(), task_server.run())


if __name__ == "__main__":
    asyncio.run(main())
