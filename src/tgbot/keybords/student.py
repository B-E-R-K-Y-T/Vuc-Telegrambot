from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard
from tgbot.utils.callback_data import CallBackData


class Student(BaseKeyboard):
    def __init__(self):
        super().__init__(
            buttons={
                "Оценки": CallBackData.MARK,
                "Посещаемость": CallBackData.ATTEND,
                "Личная информация": CallBackData.PERSONAL_DATA,
            }
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)
        return self.build_keyboard(self.buttons)
