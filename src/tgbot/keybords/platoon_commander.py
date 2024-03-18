from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard, TextButton
from tgbot.services.callback_worker.callback_data import CallBackData


class PlatoonCommander(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            buttons={
                TextButton.PLATOON_MENU: CallBackData.PLATOON_MENU,
                TextButton.SQUADS_MENU: CallBackData.VIEW_SQUADS_MENU,
                TextButton.STUDENT_MENU: CallBackData.STUDENT_MENU,
            },
            *args, **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)

        return self.build_keyboard(self.buttons)
