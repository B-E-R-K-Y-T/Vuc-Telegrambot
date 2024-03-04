from telebot.asyncio_handler_backends import State, StatesGroup


class Token(StatesGroup):
    init = State()
    end = State()
