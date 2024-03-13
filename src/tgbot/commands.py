class Command(str):
    def __init__(self, text: str):
        super().__init__(text)
        self.__text = text

    @property
    def text(self):
        return self.__text


class Commands:
    @classmethod
    def commands(cls):
        res = []

        for name_attr, type_ in cls.__dict__["__annotations__"].items():
            if type_ is Command:
                res.append(f"/{cls.__dict__[name_attr]}")

        return res


class CommandSequence(Commands):
    START: Command = "start"
    CANCEL: Command = "cancel"
    LOGIN: Command = "login"
    LOGOUT: Command = "logout"
    MENU: Command = "menu"
