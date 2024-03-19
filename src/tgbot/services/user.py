import time
from datetime import date
from typing import Optional, Any

from telebot.types import Message, CallbackQuery

from config import Roles, app_settings
from tgbot.services.api_worker.client import APIWorker
from tgbot.services.utils.collections import LimitedDict
from tgbot.services.utils.database import Database
from tgbot.services.utils.message_tools import get_message
from tgbot.services.utils.singleton import singleton


class UserState:
    pass


class UserStates:
    WORK_SELECTED_USER = UserState()


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
            token: Optional[str] = None,
            is_child: bool = False,
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
        self.__token: Optional[str] = token

        self.__selectable_user: Optional["User"] = None
        self.__count_squad_in_platoon: Optional[int] = None
        self.__semesters: Optional[int] = None
        self.__attend: Optional[list[int]] = None
        self.__is_child: bool = is_child
        self.__subordinates: dict["User.user_id", "User"] = {}
        self.__marks: dict = {}
        self.__state: Optional[UserState] = None

    async def async_init(self):
        self.__token = await self.token

        if self.__token is not None:
            self.__user_id = await self.user_id
            user = await self.api.get_user_data(self.__token, self.__user_id)
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

    async def toggle_state(self, state: UserState):
        """
        Нужно, чтобы перевести пользователя в некоторое состояние и вывести его в состояние по умолчанию, при
        обратном движении по стеку.

        Пример:
        "Меню командира отделения -> Студент 1 <ПРЕКЛЮЧАЕМСЯ В СОСТОЯНИЕ ПРОСМОТРА НЕ СВОИХ ДАННЫХ> -> Оценки"
        "Меню командира отделения <- Студент 1 <СБРАСЫВАЕМ СОСТОЯНИЕ> <- Оценки"
        """
        if self.__state != state:
            self.__state = state
        else:
            self.__state = None

    def set_state(self, state: UserState):
        self.__state = state

    def clear_state(self):
        self.__state = None

    async def add_subordinate_user(self, user: "User"):
        if await user.user_id not in self.__subordinates:
            self.__subordinates[await user.user_id] = user

    def get_subordinate_user(self, user_id) -> Optional["User"]:
        if self.__subordinates is None:
            self.__subordinates = self.get_subordinate_users()

        return self.__subordinates.get(user_id)

    async def get_subordinate_users(self) -> dict[Any, "User"]:
        if not self.__subordinates:
            _subordinates: dict = {}

            if await self.role == Roles.squad_commander:
                _subordinates = await self.api.get_students_by_squad(
                    await self.token,
                    await self.platoon_number,
                    await self.squad_number
                )
            elif await self.role == Roles.platoon_commander:
                _subordinates = await self.api.get_platoon(
                    await self.token,
                    await self.platoon_number
                )

            for subordinate in _subordinates.values():
                if await self.role == Roles.squad_commander:
                    if subordinate["role"] != Roles.student:
                        continue

                elif await self.role == Roles.platoon_commander:
                    if subordinate["role"] not in [Roles.student, Roles.squad_commander]:
                        continue

                user_id = subordinate.pop("id")
                token = await self.token

                subordinate["user_id"] = user_id
                subordinate["token"] = token
                subordinate["is_child"] = True

                user = UsersFactory().create_user_child(subordinate)

                await self.add_subordinate_user(user)

        return self.__subordinates

    async def get_user_metadata(self) -> Optional[tuple]:
        user_metadata = await self.db.get_value(key=str(self.telegram_id))

        if user_metadata is None:
            return None
        else:
            date_, jwt, email = user_metadata.decode("utf-8").split(",")

            return date_, jwt, email

    async def get_marks(self, semester: int) -> list[dict]:
        marks = await self.api.get_marks_by_semester(await self.token, await self.user_id, semester)
        res = []

        for mark in marks.values():
            res.append(mark)

        self.__marks[semester] = res

        return self.__marks[semester]

    @property
    def state(self):
        return self.__state

    @property
    async def semesters(self):
        if self.__semesters is None:
            self.__semesters = await self.api.get_semesters(await self.token, await self.user_id)

        return self.__semesters

    @property
    async def attend(self):
        _attend = await self.api.get_attend(await self.token, await self.user_id)
        temp_res = []

        for at in _attend.values():
            temp_res.append(at)

        self.__attend = temp_res

        return self.__attend

    @property
    def selectable_user(self):
        return self.__selectable_user

    @selectable_user.setter
    def selectable_user(self, value: "User"):
        self.__selectable_user = value

    @property
    async def platoon_number(self):
        if self.__platoon_number is None:
            self.__platoon_number = await self.api.get_platoon_number(await self.token, await self.user_id)

        return self.__platoon_number

    @property
    async def name(self):
        if self.__name is None:
            self.__name = await self.api.get_user_name(await self.token, await self.user_id)

        return self.__name

    @property
    async def squad_number(self):
        if self.__squad_number is None:
            self.__squad_number = await self.api.get_squad_user(await self.token, await self.user_id)

        return self.__squad_number

    @property
    async def group_study(self):
        if self.__group_study is None:
            self.__group_study = await self.api.get_user_group_study(await self.token, await self.user_id)

        return self.__group_study

    @property
    async def address(self):
        if self.__address is None:
            self.__address = await self.api.get_user_address(await self.token, await self.user_id)

        return self.__address

    @property
    async def count_squad_in_platoon(self):
        if self.__count_squad_in_platoon is None:
            self.__count_squad_in_platoon = await self.api.get_count_squad_in_platoon(
                await self.token,
                await self.platoon_number)

        return self.__count_squad_in_platoon

    @property
    async def direction_of_study(self):
        if self.__direction_of_study is None:
            self.__direction_of_study = await self.api.get_user_direction_of_study(
                await self.token,
                await self.user_id
            )

        return self.__direction_of_study

    @property
    def telegram_id(self):
        return self.__telegram_id

    @property
    async def user_id(self):
        if self.__user_id is None:
            if await self.token is not None:
                self.__user_id: int = await self.api.get_id_from_email(
                    await self.token, await self.email
                )

        return self.__user_id

    @property
    async def role(self) -> str:
        if self.__role is None:
            self.__role: str = await self.api.get_user_role(await self.token, await self.user_id)

        return self.__role

    @property
    async def token(self) -> str | None:
        if self.__is_child and self.__token is not None:
            return self.__token

        now = time.time()
        user_metadata = await self.get_user_metadata()

        if user_metadata is None:
            return None

        date_, jwt, _ = user_metadata

        if now - int(date_) > app_settings.TIME_LIFE_SESSION:
            await self.db.del_value(key=str(self.telegram_id))
            return None

        return jwt

    async def delete_token(self):
        await self.db.del_value(key=str(self.telegram_id))

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
        self.__users: LimitedDict[int, tuple[User, int]] = LimitedDict()

    async def get_user(self, metadata: Message | CallbackQuery) -> User:
        telegram_id: int = get_message(metadata).chat.id

        return await self.get_actual_user(telegram_id)

    async def get_actual_user(self, telegram_id: int) -> User:
        now: float = time.time()
        user_state: Optional[UserState] = None
        selectable_user: Optional[User] = None

        if telegram_id in self.__users:
            user, created_at = self.__users.get(telegram_id)

            if user is not None:
                if now - created_at > app_settings.TIME_LIFE_CACHE_USERS:
                    old_user_image, _ = self.__users[telegram_id]
                    user_state = old_user_image.state
                    selectable_user = old_user_image.selectable_user

                    del self.__users[telegram_id]

        actual_user: User = await self.get_user_by_telegram_id(telegram_id)

        if actual_user.state is None:
            actual_user.set_state(user_state)

        if actual_user.selectable_user is None:
            actual_user.selectable_user = selectable_user

        return actual_user

    async def get_user_by_telegram_id(self, telegram_id: int) -> User:
        if telegram_id not in self.__users:
            created_at = time.time()
            user = await User(telegram_id=telegram_id).async_init()

            self.__users[telegram_id] = user, created_at

        user = self.__users[telegram_id][0]

        return user

    @staticmethod
    def create_user_child(user_image: dict) -> User:
        user = User(**user_image)

        return user

    async def delete_user(self, telegram_id: int) -> None:
        if telegram_id in self.__users:
            user = await self.get_user_by_telegram_id(telegram_id)
            await user.delete_token()

            del self.__users[telegram_id]
