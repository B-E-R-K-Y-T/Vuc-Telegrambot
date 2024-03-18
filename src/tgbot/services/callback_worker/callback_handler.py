from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from exceptions import FunctionStackEmpty, StackRoot
from tgbot.services.callback_worker.callback_stack import StackStrider
from tgbot.handlers.menu.inline_menu import self_menu, function_stack, stack_builder, semesters_menu, send_marks, \
    menu_handler, send_personal_info, personal_menu, view_attend, squad_commander_start_menu, view_squad_menu, \
    view_squads_menu
from tgbot.services.api_worker.client import APIWorker
from tgbot.services.commands import CommandSequence
from tgbot.services.user import User, UsersFactory
from tgbot.services.utils.message_tools import get_message
from tgbot.services.callback_worker.callback_data import CallBackData
from tgbot.handlers.setters_pd import (
    init_dob_state,
    init_dos_state,
    init_name_state,
    init_email_state,
    init_phone_state,
    init_address_state,
    init_institute_state,
    init_group_study_state,
)


async def callback_handler(call: CallbackQuery, bot: AsyncTeleBot):
    message: Message = get_message(call)
    user: User = await UsersFactory().get_user(message)
    stack_strider = StackStrider(function_stack, stack_builder)
    api = APIWorker()

    semesters_map = {
        CallBackData.SEMESTER_ONE: 1,
        CallBackData.SEMESTER_TWO: 2,
        CallBackData.SEMESTER_THREE: 3,
        CallBackData.SEMESTER_FOUR: 4,
        CallBackData.SEMESTER_FIVE: 5,
        CallBackData.SEMESTER_SIX: 6,
    }
    squads_buttons_map = {
        CallBackData.SQUAD_ONE: 1,
        CallBackData.SQUAD_TWO: 2,
        CallBackData.SQUAD_THREE: 3
    }


    if call.data == CallBackData.BACK:
        try:
            await stack_strider.back(message.chat.id, message.message_id)
        except StackRoot as _:
            await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)
        except FunctionStackEmpty as _:
            await bot.send_message(
                message.chat.id,
                f"История пуста. Попробуйте открыть меню ещё раз: /{CommandSequence.MENU}"
            )

    elif call.data == CallBackData.REOPEN_MENU:
        await menu_handler(message, bot)
        function_stack.clear_message_stack(message.chat.id, message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    elif call.data == CallBackData.STUDENT_MENU:
        await self_menu(message, bot)

    elif call.data == CallBackData.MARK:
        await semesters_menu(message, bot, user)

    elif call.data == CallBackData.PERSONAL_DATA:
        await send_personal_info(message, bot)

    elif call.data in semesters_map:
        await send_marks(message, bot, user, semester=semesters_map[call.data])

    elif call.data == CallBackData.EDIT_PERSONAL_DATA:
        await personal_menu(message, bot)

    elif call.data == CallBackData.ATTEND:
        await view_attend(message, bot, user)

    elif call.data == CallBackData.EMAIL:
        await init_email_state(call, bot)

    elif call.data == CallBackData.DOB:
        await init_dob_state(call, bot)

    elif call.data == CallBackData.DOS:
        await init_dos_state(call, bot)

    elif call.data == CallBackData.NAME:
        await init_name_state(call, bot)

    elif call.data == CallBackData.EMAIL:
        await init_email_state(call, bot)

    elif call.data == CallBackData.PHONE:
        await init_phone_state(call, bot)

    elif call.data == CallBackData.ADDRESS:
        await init_address_state(call, bot)

    elif call.data == CallBackData.INSTITUTE:
        await init_institute_state(call, bot)

    elif call.data == CallBackData.GROUP_STUDY:
        await init_group_study_state(call, bot)

    elif call.data in CallBackData.VIEW_SQUADS_MENU:
        await view_squads_menu(message, bot, user)

    elif call.data in squads_buttons_map:
        await view_squad_menu(message, bot, user, squads_buttons_map[call.data])
