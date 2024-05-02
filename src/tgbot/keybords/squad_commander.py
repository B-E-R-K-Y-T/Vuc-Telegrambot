from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard, TextButton
from tgbot.services.callback_worker.callback_data import CallBackData


class SquadCommander(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.buttons = {
            TextButton.SQUADS_MENU: CallBackData.SQUAD_MENU,
            TextButton.STUDENT_MENU: CallBackData.STUDENT_MENU,
        }

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)

        return self.build_keyboard(self.buttons)
