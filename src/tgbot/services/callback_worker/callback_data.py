import hashlib

from typing import Optional

from telebot.types import CallbackQuery

PREFIX_SEPARATOR: str = hashlib.md5(b".").hexdigest()


class _auto_callback_data:
    state = 0

    def __new__(cls, *args, **kwargs):
        cls.state += 1

        return f"{CallBackPrefix.CALLBACK}{cls.state}"


def get_callback_payload(call: CallbackQuery) -> Optional[str]:
    if PREFIX_SEPARATOR in call.data:
        data: list[str] = call.data.split(PREFIX_SEPARATOR)

        if len(data) > 1:
            return data[1]

    return None


class CallBackPrefix:
    STUDENT = f"student{PREFIX_SEPARATOR}"
    CALLBACK = f"callback{PREFIX_SEPARATOR}"
    EDIT_STUDENT = f"edit_student{PREFIX_SEPARATOR}"


class CallBackData:
    MARK = _auto_callback_data()
    MARK_VIEW_FROM_STUDENT_TO_COMMANDER = _auto_callback_data()
    ATTEND = _auto_callback_data()
    ATTEND_VIEW_FROM_COMMANDER = _auto_callback_data()
    EDIT_ATTEND_OF_STUDENT = _auto_callback_data()
    SET_ATTEND = _auto_callback_data()
    SET_POSITIVE_ATTEND = _auto_callback_data()
    SET_NEGATIVE_ATTEND = _auto_callback_data()
    EDIT_PERSONAL_DATA = _auto_callback_data()
    PERSONAL_DATA = _auto_callback_data()

    SEMESTER_ONE = _auto_callback_data()
    SEMESTER_TWO = _auto_callback_data()
    SEMESTER_THREE = _auto_callback_data()
    SEMESTER_FOUR = _auto_callback_data()
    SEMESTER_FIVE = _auto_callback_data()
    SEMESTER_SIX = _auto_callback_data()

    SQUAD_ONE = _auto_callback_data()
    SQUAD_TWO = _auto_callback_data()
    SQUAD_THREE = _auto_callback_data()

    STUDENT_MENU = _auto_callback_data()
    VIEW_SQUADS_MENU = _auto_callback_data()
    SQUAD_MENU = _auto_callback_data()
    PLATOON_MENU = _auto_callback_data()

    ADD_STUDENT = _auto_callback_data()
    MOVE_STUDENT = _auto_callback_data()

    NAME = _auto_callback_data()
    DOB = _auto_callback_data()
    PHONE = _auto_callback_data()
    EMAIL = _auto_callback_data()
    ADDRESS = _auto_callback_data()
    INSTITUTE = _auto_callback_data()
    DOS = _auto_callback_data()
    GROUP_STUDY = _auto_callback_data()
    PLATOON_NUMBER = _auto_callback_data()
    SQUAD_NUMBER = _auto_callback_data()
    ROLE = _auto_callback_data()
    TELEGRAM_ID = _auto_callback_data()

    BACK = _auto_callback_data()
    REOPEN_MENU = _auto_callback_data()


__all__ = (
    CallBackData.__name__,
    CallBackPrefix.__name__,
    get_callback_payload.__name__,
    "PREFIX_SEPARATOR",
)
