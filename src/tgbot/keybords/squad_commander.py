from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard
from tgbot.utils.callback_data import CallBackData


class SquadCommander(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            buttons={
                "Меню командира отделения": CallBackData.SQUAD_MENU,
                "Меню студента": CallBackData.STUDENT_MENU,
            },
            *args, **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)

        return self.build_keyboard(self.buttons)
