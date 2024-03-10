class _auto_callback_data:
    state = 0

    def __new__(cls, *args, **kwargs):
        self = object.__new__(cls)

        cls.state += 1

        return self()

    def __call__(self):
        return self.state


class CallBackData:
    MARK = _auto_callback_data()
    ATTEND = _auto_callback_data()
    SELF_DATA = _auto_callback_data()

    SEMESTER_ONE = _auto_callback_data()
    SEMESTER_TWO = _auto_callback_data()


__all__ = (
    CallBackData.__name__,
)
