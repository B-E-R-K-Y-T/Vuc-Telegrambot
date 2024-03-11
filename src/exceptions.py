from telebot.async_telebot import ExceptionHandler

from logger import LOGGER


class MainVucException(Exception):
    def __init__(self, message=None, *args):
        super().__init__(*args)

        if message is not None:
            self.__message = message
        else:
            self.__message = (
                f"Error. Detail: {self.__class__=}"
            )

    def __str__(self):
        return self.__message


class EmailError(MainVucException):
    pass


class VucExceptionHandler(ExceptionHandler):
    async def handle(self, exception):
        LOGGER.err(exception)


class ErrorMessage:
    EMAIL_INVALID_FORMAT = 'Не верный формат электронной почты.'
