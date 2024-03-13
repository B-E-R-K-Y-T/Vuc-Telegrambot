from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard
from tgbot.utils.callback_data import CallBackData


class PlatoonButtons(BaseKeyboard):
    def __init__(self):
        super().__init__(
            buttons={
                "Добавить студента": CallBackData.ADD_STUDENT,
                "Перемесить студента в др. отделение": CallBackData.MOVE_STUDENT,
                "Назад": CallBackData.BACK,
            }
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)

        return self.build_keyboard(self.buttons)
