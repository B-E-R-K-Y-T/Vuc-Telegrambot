from typing import Optional

from tgbot.keybords.base_keyboard import BaseKeyboard
from tgbot.utils.callback_data import CallBackData


class PersonalDataButtons(BaseKeyboard):
    def __init__(self):
        super().__init__(
            buttons={
                "ФИО": CallBackData.NAME,
                "День рождения": CallBackData.DOB,
                "Номер телефона": CallBackData.PHONE,
                "Почта": CallBackData.EMAIL,
                "Адрес": CallBackData.ADDRESS,
                "Институт": CallBackData.INSTITUTE,
                "Направление обучения": CallBackData.DOS,
                "Группа обучения": CallBackData.GROUP_STUDY,
                "Назад": CallBackData.BACK,
            }
        )

    def menu(self, new_buttons: Optional[dict] = None):
        self.update_buttons(new_buttons)

        return self.build_keyboard(self.buttons)
