from telebot.async_telebot import AsyncTeleBot
from telebot.types import CallbackQuery, Message

from exceptions import FunctionCallStackEmpty, AchievedStackRoot
from tgbot.keybords.base_keyboard import BaseKeyboard
from tgbot.services.callback_worker.callback_stack import StackStrider
from tgbot.handlers.menu.inline_menu import (
    self_menu,
    function_stack,
    stack_builder,
    semesters_menu,
    send_marks,
    menu_handler,
    send_personal_info,
    personal_menu,
    view_attend,
    view_squad_menu,
    view_squads_menu,
    edit_student_from_commander,
    mark_view_from_student_to_commander,
    edit_attend,
    set_attend_menu,
    set_positive_attend_state,
    set_negative_attend_state,
    view_platoon_menu,
)
from tgbot.services.api_worker.client import APIWorker
from tgbot.services.date_tools.next_date import get_tomorrow_date
from tgbot.services.user import User, UsersFactory, UserStates
from tgbot.services.utils.message_tools import get_message, send_temp_smile
from tgbot.services.callback_worker.callback_data import (
    CallBackData,
    CallBackPrefix,
    get_callback_payload,
)
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
    current_user: User = await UsersFactory().get_user(message)
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
        CallBackData.SQUAD_THREE: 3,
    }

    if call.data == CallBackData.BACK:
        try:
            await stack_strider.back(message.chat.id, message.message_id)
        except AchievedStackRoot as _:
            await bot.delete_message(
                chat_id=message.chat.id, message_id=message.message_id
            )
        except FunctionCallStackEmpty as _:
            markup_refresh = BaseKeyboard(back_button_on=False).menu()

            await bot.send_message(
                message.chat.id,
                f"История пуста. Попробуйте открыть меню ещё раз.",
                reply_markup=markup_refresh
            )

    elif call.data == CallBackData.REOPEN_MENU:
        await menu_handler(message, bot)
        function_stack.clear_message_stack(message.chat.id, message.message_id)
        await bot.delete_message(chat_id=message.chat.id, message_id=message.message_id)

    elif call.data == CallBackData.STUDENT_MENU:
        current_user.clear_state()
        await self_menu(message, bot)

    elif call.data == CallBackData.MARK:
        await semesters_menu(message, bot, current_user)

    elif call.data == CallBackData.MARK_VIEW_FROM_STUDENT_TO_COMMANDER:
        await mark_view_from_student_to_commander(message, bot, current_user.selectable_user)

    elif call.data == CallBackData.PERSONAL_DATA:
        await send_personal_info(message, bot)

    elif call.data in semesters_map:
        if current_user.state == UserStates.WORK_SELECTED_USER:
            await send_marks(message, bot, current_user.selectable_user, semester=semesters_map[call.data])
        else:
            await send_marks(message, bot, current_user, semester=semesters_map[call.data])

    elif call.data == CallBackData.EDIT_PERSONAL_DATA:
        await personal_menu(message, bot)

    elif call.data == CallBackData.ATTEND:
        await view_attend(message, bot, current_user)

    elif call.data == CallBackData.ATTEND_VIEW_FROM_COMMANDER:
        if current_user.state == UserStates.WORK_SELECTED_USER:
            await view_attend(message, bot, current_user.selectable_user)
        else:
            await send_temp_smile(message, bot, "❌")

    elif call.data == CallBackData.EDIT_ATTEND_OF_STUDENT:
        if current_user.state == UserStates.WORK_SELECTED_USER:
            await edit_attend(message, bot)
        else:
            await send_temp_smile(message, bot, "❌")

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
        await view_squads_menu(message, bot, current_user)

    elif call.data in squads_buttons_map:
        await view_squad_menu(message, bot, current_user, squads_buttons_map[call.data])

    elif call.data.startswith(CallBackPrefix.EDIT_STUDENT):
        target_user_telegram_id: int = int(get_callback_payload(call))
        select_user: User = current_user.get_subordinate_user(target_user_telegram_id)
        current_user.selectable_user = select_user

        await edit_student_from_commander(message, bot)

    elif call.data == CallBackData.SET_ATTEND:
        if current_user.state == UserStates.WORK_SELECTED_USER:
            await set_attend_menu(message, bot)
        else:
            await send_temp_smile(message, bot, "❌")

    elif call.data == CallBackData.SET_POSITIVE_ATTEND:
        if current_user.state == UserStates.WORK_SELECTED_USER:
            await set_positive_attend_state(message, bot)
        else:
            await send_temp_smile(message, bot, "❌")

    elif call.data == CallBackData.SET_NEGATIVE_ATTEND:
        if current_user.state == UserStates.WORK_SELECTED_USER:
            await set_negative_attend_state(message, bot)
        else:
            await send_temp_smile(message, bot, "❌")

    elif call.data == CallBackData.PLATOON_MENU:
        await view_platoon_menu(message, bot)
    elif call.data == CallBackPrefix.ATTEND_STUDENT_NEGATIVE:
        r = await api.set_visit_user(
            token=await current_user.token,
            date_v=str(get_tomorrow_date()),
            visiting=0,
            user_id=await current_user.user_id
        )
        print(r)

    elif call.data == CallBackPrefix.ATTEND_STUDENT_POSITIVE:
        await api.set_visit_user(
            token=await current_user.token,
            date_v=str(get_tomorrow_date()),
            visiting=1,
            user_id=await current_user.user_id
        )
