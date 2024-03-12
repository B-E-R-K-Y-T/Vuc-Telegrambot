class Command(str):
    def __init__(self, text: str):
        self.__text = text

    @property
    def text(self):
        return self.__text


class Commands:
    @classmethod
    def commands(cls):
        names = []

        for name_attr, type_ in cls.__dict__['__annotations__'].items():
            if type_ is Command:
                names.append(name_attr)

        res = []

        for name in names:
            res.append(f'/{cls.__dict__[name]}')

        return res


class CommandSequence(Commands):
    START: Command = 'start'
    CANCEL: Command = 'cancel'
    LOGIN: Command = 'login'
    LOGOUT: Command = 'logout'
    MENU: Command = 'menu'
    TEST: Command = 'test'
