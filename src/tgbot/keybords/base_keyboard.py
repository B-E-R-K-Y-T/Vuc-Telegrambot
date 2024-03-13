from abc import ABC, abstractmethod
from typing import Optional

from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton


class BaseKeyboard(ABC):
    def __init__(self, buttons: Optional[dict] = None):
        self.buttons: Optional[dict] = buttons

    @staticmethod
    def build_keyboard(buttons: dict, row_width: int = 3) -> InlineKeyboardMarkup:
        keyboard = InlineKeyboardMarkup(row_width=row_width)

        for name, callback in buttons.items():
            keyboard.add(InlineKeyboardButton(text=name, callback_data=callback))

        return keyboard

    def update_buttons(self, new_buttons: Optional[dict] = None):
        if new_buttons is not None:
            self.buttons.update(new_buttons)

    @abstractmethod
    def menu(self) -> InlineKeyboardMarkup:
        raise NotImplementedError
