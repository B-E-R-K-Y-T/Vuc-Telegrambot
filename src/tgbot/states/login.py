from telebot.asyncio_handler_backends import StatesGroup, State


class Login(StatesGroup):
    email = State()
    password = State()
