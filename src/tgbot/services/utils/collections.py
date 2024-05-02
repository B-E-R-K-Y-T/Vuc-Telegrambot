from collections import OrderedDict


class LimitedDict(OrderedDict):
    def __init__(self, *args, max_len: int = 200, **kwargs):
        super(LimitedDict, self).__init__(*args, **kwargs)
        self.__max_len: int = max_len

    def __refresh_dict(self):
        if len(self) >= self.__max_len:
            self.popitem(last=False)

    def __setitem__(self, key, value):
        self.__refresh_dict()

        super(LimitedDict, self).__setitem__(key, value)

    def setdefault(self, key, default=None):
        self.__refresh_dict()

        super(LimitedDict, self).setdefault(key, default)


__all__ = (LimitedDict.__name__,)
