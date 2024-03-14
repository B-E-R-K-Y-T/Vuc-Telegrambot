from telebot.asyncio_handler_backends import StatesGroup, State


class SetName(StatesGroup):
    init = State()


class SetDob(StatesGroup):
    init = State()


class SetPhone(StatesGroup):
    init = State()


class SetEmail(StatesGroup):
    init = State()


class SetAddress(StatesGroup):
    init = State()


class SetInstitute(StatesGroup):
    init = State()


class SetDos(StatesGroup):
    init = State()


class SetGroupStudy(StatesGroup):
    init = State()


__all__ = (
    SetDos.__name__,
    SetEmail.__name__,
    SetPhone.__name__,
    SetAddress.__name__,
    SetInstitute.__name__,
    SetDob.__name__,
    SetGroupStudy.__name__,
    SetName.__name__,
)
