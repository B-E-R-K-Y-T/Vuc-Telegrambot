from telebot.asyncio_handler_backends import StatesGroup, State


class SetName(StatesGroup):
    init = State()
    end = State()
