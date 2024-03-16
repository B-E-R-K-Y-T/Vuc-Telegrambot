import asyncio

from telebot import asyncio_filters
from telebot.async_telebot import AsyncTeleBot
from telebot.asyncio_storage import StateMemoryStorage

from tgbot.services.commands import CommandSequence
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
from tgbot.handlers.inline_menu import (
    menu_handler,
    student_menu,
    back,
    platoon_menu,
    marks_menu,
    view_attend,
    personal_menu,
    send_marks,
    reopen_menu,
    view_pd,
    view_squads_menu,
    view_squad_menu,
    squad_commander_menu,
)
from tgbot.handlers.outline_menu import handle_outline_output
from tgbot.handlers.self import self
from tgbot.handlers.setters_pd import (
    init_email_state,
    init_dos_state,
    init_phone_state,
    init_address_state,
    init_institute_state,
    init_group_study_state,
    init_name_state,
    init_dob_state,
    set_dos,
    set_phone,
    set_address,
    set_institute,
    set_dob,
    set_group_study,
    set_name,
    set_email,
)
from tgbot.handlers.start import start_command_handler
from tgbot.middlewares.antiflood_middleware import AntiFloodMiddleware
from config import app_settings
from tgbot.services.outline_text_buttons import OutlineKeyboardButton
from tgbot.states.login import Login
from tgbot.states.setter_states import *
from tgbot.services.utils.callback_data import CallBackData

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
        student_menu,
        func=lambda call: call.data == CallBackData.STUDENT_MENU,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        squad_commander_menu,
        func=lambda call: call.data == CallBackData.SQUAD_MENU,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        view_squads_menu,
        func=lambda call: call.data == CallBackData.VIEW_SQUADS_MENU,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        view_squad_menu,
        func=lambda call: call.data == CallBackData.SQUAD_ONE,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        view_squad_menu,
        func=lambda call: call.data == CallBackData.SQUAD_TWO,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        view_squad_menu,
        func=lambda call: call.data == CallBackData.SQUAD_THREE,
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
        view_attend,
        func=lambda call: call.data == CallBackData.ATTEND,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        personal_menu,
        func=lambda call: call.data == CallBackData.EDIT_PERSONAL_DATA,
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

    # Сеттеры персональных данных
    init_base_filters(
        init_name_state,
        func=lambda call: call.data == CallBackData.NAME,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(set_name, pass_bot=True, state=SetName.init)

    init_base_filters(
        init_dob_state,
        func=lambda call: call.data == CallBackData.DOB,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(set_dob, pass_bot=True, state=SetDob.init)

    init_base_filters(
        init_group_study_state,
        func=lambda call: call.data == CallBackData.GROUP_STUDY,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(set_group_study, pass_bot=True, state=SetGroupStudy.init)

    init_base_filters(
        init_phone_state,
        func=lambda call: call.data == CallBackData.PHONE,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(set_phone, pass_bot=True, state=SetPhone.init)

    init_base_filters(
        init_address_state,
        func=lambda call: call.data == CallBackData.ADDRESS,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(set_address, pass_bot=True, state=SetAddress.init)

    init_base_filters(
        init_email_state,
        func=lambda call: call.data == CallBackData.EMAIL,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(set_email, pass_bot=True, state=SetEmail.init)

    init_base_filters(
        init_dos_state,
        func=lambda call: call.data == CallBackData.DOS,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(set_dos, pass_bot=True, state=SetDos.init)

    init_base_filters(
        init_institute_state,
        func=lambda call: call.data == CallBackData.INSTITUTE,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(set_institute, pass_bot=True, state=SetInstitute.init)
    # ------------------------------------------------------------------------------------------------------------------

    # Handler marks buttons
    init_base_filters(
        send_marks,
        func=lambda call: call.data == CallBackData.SEMESTER_ONE,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        send_marks,
        func=lambda call: call.data == CallBackData.SEMESTER_TWO,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        send_marks,
        func=lambda call: call.data == CallBackData.SEMESTER_THREE,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        send_marks,
        func=lambda call: call.data == CallBackData.SEMESTER_FOUR,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        send_marks,
        func=lambda call: call.data == CallBackData.SEMESTER_FIVE,
        callback_query_flag=True,
        pass_bot=True,
    )
    init_base_filters(
        send_marks,
        func=lambda call: call.data == CallBackData.SEMESTER_SIX,
        callback_query_flag=True,
        pass_bot=True,
    )
    # ------------------------------------------------------------------------------------------------------------------

    init_base_filters(
        reopen_menu,
        func=lambda call: call.data == CallBackData.REOPEN_MENU,
        callback_query_flag=True,
        pass_bot=True,
    )

    init_base_filters(
        view_pd,
        func=lambda call: call.data == CallBackData.PERSONAL_DATA,
        callback_query_flag=True,
        pass_bot=True,
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
