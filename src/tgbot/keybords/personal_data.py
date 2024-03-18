from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard, TextButton
from tgbot.services.callback_worker.callback_data import CallBackData


class PersonalDataButtons(BaseKeyboard):
    def __init__(self, *args, **kwargs):
        super().__init__(
            buttons={
                TextButton.NAME: CallBackData.NAME,
                TextButton.DOB: CallBackData.DOB,
                TextButton.PHONE: CallBackData.PHONE,
                TextButton.ADDRESS: CallBackData.ADDRESS,
                TextButton.INSTITUTE: CallBackData.INSTITUTE,
                TextButton.DOS: CallBackData.DOS,
                TextButton.GROUP_STUDY: CallBackData.GROUP_STUDY,
            },
            *args, **kwargs
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)

        return self.build_keyboard(self.buttons)
