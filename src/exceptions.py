from telebot.async_telebot import ExceptionHandler

from logger import LOGGER


class MainVucException(Exception):
    def __init__(self, message=None, *args):
        super().__init__(*args)

        if message is not None:
            self.__message = message
        else:
            self.__message = f"Error. Detail: {self.__class__=}"

    def __str__(self):
        return self.__message


class EmailError(MainVucException):
    pass


class VucExceptionHandler(ExceptionHandler):
    async def handle(self, exception):
        LOGGER.err(exception)


class ErrorMessage:
    EMAIL_INVALID_FORMAT = "Не верный формат электронной почты."
    PHONE_INVALID_FORMAT = ("Не верный формат номера телефона.\n\n"
                            "Телефон должен быть в одном из таких форматов:\n\n"
                            "+7 800 555 35 35\n8 800 555 35 35\n88005553535\n+7 (800) 555-35-35")
    GROUP_STUDY_INVALID_FORMAT = ("Не верный формат группы обучения.\n\n"
                                  "Группа должна быть в таком формате: БСБО-08-19")
    DATE_INVALID_FORMAT = ("Не верный формат даты.\n\n"
                           "Дата должна быть в таком формате: 27.09.2001")
