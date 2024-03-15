import time
from datetime import date
from typing import Optional, Dict, Any

from telebot.types import Message, CallbackQuery

from tgbot.api_worker.client import APIWorker
from tgbot.utils.collections import LimitedDict
from tgbot.utils.database import Database
from tgbot.utils.message_tools import get_message
from tgbot.utils.singleton import singleton


class User:
    def __init__(
            self,
            telegram_id: int,
            email: Optional[str] = None,
            password: Optional[str] = None,
            user_id: Optional[int] = None,
            date_of_birth: Optional[str] = None,
            phone: Optional[str] = None,
            address: Optional[str] = None,
            institute: Optional[str] = None,
            direction_of_study: Optional[str] = None,
            group_study: Optional[str] = None,
            platoon_number: Optional[int] = None,
            squad_number: Optional[int] = None,
            role: Optional[str] = None,
            name: Optional[str] = None,
    ):
        self.db = Database()
        self.api = APIWorker()

        self.__telegram_id: int = telegram_id
        self.__email: Optional[str] = email
        self.__password: Optional[str] = password
        self.__user_id: Optional[int] = user_id
        self.__date_of_birth: Optional[date] = date_of_birth
        self.__phone: Optional[str] = phone
        self.__address: Optional[str] = address
        self.__institute: Optional[str] = institute
        self.__direction_of_study: Optional[str] = direction_of_study
        self.__group_study: Optional[str] = group_study
        self.__platoon_number: Optional[int] = platoon_number
        self.__squad_number: Optional[int] = squad_number
        self.__role: Optional[str] = role
        self.__name: Optional[str] = name

        self.__token: Optional[str] = None
        self.__subordinates: dict["User.user_id", "User"] = {}

    async def async_init(self):
        self.__token = await self.token

        if self.__token is not None:
            self.__user_id = await self.user_id
            user = await self.api.get_self(self.__token, self.__user_id)

            tmp_date = str(user.get("date_of_birth")).split('T')[0]

            year, month, day = [int(item) for item in tmp_date.split('-')]

            self.__date_of_birth: Optional[date] = date(year, month, day)
            self.__phone: Optional[str] = user.get("phone")
            self.__email: Optional[str] = user.get("email")
            self.__address: Optional[str] = user.get("address")
            self.__institute: Optional[str] = user.get("institute")
            self.__direction_of_study: Optional[str] = user.get("direction_of_study")
            self.__group_study: Optional[str] = user.get("group_study")
            self.__platoon_number: Optional[int] = user.get("platoon_number")
            self.__squad_number: Optional[int] = user.get("squad_number")
            self.__role: Optional[str] = user.get("role")

        return self

    async def add_subordinate_user(self, user: "User"):
        if await user.user_id not in self.__subordinates:
            self.__subordinates[await user.user_id] = user

    def get_subordinate_user(self, user_id) -> Optional["User"]:
        return self.__subordinates.get(user_id)

    def get_subordinate_users(self) -> dict[Any, "User"]:
        return self.__subordinates

    async def get_user_metadata(self) -> tuple | None:
        user_metadata = await self.db.get_value(key=str(self.telegram_id))

        if user_metadata is None:
            return None
        else:
            date_, jwt, email = user_metadata.decode("utf-8").split(",")

            return date_, jwt, email

    @property
    async def platoon_number(self):
        if self.__platoon_number is None:
            self.__platoon_number = await self.api.get_platoon_number(self.__token, self.__user_id)

        return self.__platoon_number

    @property
    async def name(self):
        if self.__name is None:
            self.__name = await self.api.get_user_name(self.__token, self.__user_id)

        return self.__name

    @property
    async def squad_number(self):
        if self.__squad_number is None:
            self.__squad_number = await self.api.get_squad_user(self.__token, self.__user_id)

        return self.__squad_number

    @property
    async def group_study(self):
        if self.__group_study is None:
            self.__group_study = await self.api.get_user_group_study(self.__token, self.__user_id)

        return self.__group_study

    @property
    async def address(self):
        if self.__address is None:
            self.__address = await self.api.get_user_address(self.__token, self.__user_id)

        return self.__address

    @property
    async def direction_of_study(self):
        if self.__direction_of_study is None:
            self.__direction_of_study = await self.api.get_user_direction_of_study(self.__token, self.__user_id)

        return self.__direction_of_study

    @property
    def telegram_id(self):
        return self.__telegram_id

    @property
    async def user_id(self):
        if self.__user_id is None:
            self.__token = await self.token

            if self.__token is not None:
                self.__user_id: int = await self.api.get_id_from_email(
                    self.__token, await self.email
                )

        return self.__user_id

    @property
    async def role(self) -> str:
        if self.__role is None:
            self.__role: str = await self.api.get_user_role(await self.token, await self.user_id)

        return self.__role

    @property
    async def token(self) -> str | None:
        now = time.time()
        user_metadata = await self.get_user_metadata()

        if user_metadata is None:
            return None

        date_, jwt, _ = user_metadata

        if now - int(date_) > 3600:
            await self.db.del_value(key=str(self.telegram_id))
            return None

        return jwt

    @property
    async def email(self) -> str | None:
        if self.__email is None:
            user_metadata = await self.get_user_metadata()

            if user_metadata is None:
                return None
            else:
                _, _, self.__email = user_metadata

                return self.__email
        else:
            return self.__email

    def set_email(self, value: str):
        self.__email = value

    @property
    def password(self) -> str:
        return self.__password

    @password.setter
    def password(self, value: str):
        self.__password = value


@singleton
class UsersFactory:
    def __init__(self):
        self.__users: LimitedDict = LimitedDict()

    async def get_user(self, metadata: Message | CallbackQuery) -> User:
        telegram_id: int = get_message(metadata).chat.id

        if telegram_id not in self.__users:
            user = await User(telegram_id=telegram_id).async_init()
            self.__users[telegram_id] = user

        return self.__users[telegram_id]

    def create_user(self, data: dict) -> User:
        telegram_id: int = data.get("telegram_id")

        if telegram_id not in self.__users:
            user = User(**data)
            self.__users[telegram_id] = user

        return self.__users[telegram_id]
