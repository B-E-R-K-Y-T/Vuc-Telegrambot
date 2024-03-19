from telebot.asyncio_handler_backends import StatesGroup, State


class PositiveAttend(StatesGroup):
    init = State()


class NegativeAttend(StatesGroup):
    init = State()
