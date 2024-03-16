from tgbot.services.collector_fields import CollectorField


class Command(str):
    def __init__(self, text: str):
        super().__init__(text)
        self.__text = text

    @property
    def text(self):
        return self.__text


class Commands(CollectorField):
    field_type = Command

    @classmethod
    def fields(cls):
        commands = super().fields()

        return [f'/{cmd}' for cmd in commands]


class CommandSequence(Commands):
    START: Command = "start"
    CANCEL: Command = "cancel"
    LOGIN: Command = "login"
    LOGOUT: Command = "logout"
    MENU: Command = "menu"
    SELF: Command = "self"
