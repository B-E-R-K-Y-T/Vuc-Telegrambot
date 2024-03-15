from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard
from tgbot.utils.callback_data import CallBackData


class Student(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            buttons={
                "Оценки": CallBackData.MARK,
                "Посещаемость": CallBackData.ATTEND,
                "Персональные данные": CallBackData.PERSONAL_DATA,
                "Изменить персональные данные": CallBackData.EDIT_PERSONAL_DATA,
            },
            *args, **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)
        return self.build_keyboard(self.buttons)
