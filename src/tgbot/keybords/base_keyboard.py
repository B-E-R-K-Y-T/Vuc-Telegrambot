from typing import Optional

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from tgbot.utils.callback_data import CallBackData


class TextButton:
    BACK = '⬅️'
    REOPEN = '🔄'


class BaseKeyboard:
    def __init__(
            self,
            buttons: Optional[dict] = None,
            reopen_menu_button_on: bool = True,
            back_button_on: bool = True
    ):
        if buttons is None:
            self.buttons: dict = {}
        else:
            self.buttons: dict = buttons

        self.reopen_menu_button_on = reopen_menu_button_on
        self.back_button_on = back_button_on

    def build_keyboard(self, buttons: dict, row_width: int = 3) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=row_width)

        for name, callback in buttons.items():
            keyboard.add(InlineKeyboardButton(text=name, callback_data=callback))

        move_buttons = []

        if self.back_button_on:
            move_buttons.append(InlineKeyboardButton(text=TextButton.BACK, callback_data=CallBackData.BACK))

        if self.reopen_menu_button_on:
            move_buttons.append(InlineKeyboardButton(text=TextButton.REOPEN, callback_data=CallBackData.REOPEN_MENU))

        if move_buttons:
            keyboard.add(*move_buttons)

        return keyboard

    def update_buttons(self, new_buttons: Optional[dict] = None):
        if new_buttons is not None:
            if self.buttons is None:
                self.buttons = new_buttons.copy()
            else:
                self.buttons.update(new_buttons)

    def menu(self, new_buttons: Optional[dict] = None) -> InlineKeyboardMarkup:
        self.update_buttons(new_buttons)

        return self.build_keyboard(self.buttons)
