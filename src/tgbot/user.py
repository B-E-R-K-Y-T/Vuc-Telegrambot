import time
from typing import Optional

from tgbot.api_worker.client import APIWorker
from tgbot.utils.database import Database


class User:
    def __init__(self, tg_id: int):
        self.tg_id: int = tg_id
        self.__email = None
        self.__password = None
        self.db = Database()
        self.api = APIWorker()
        self.user_id: Optional[int] = None

    async def ainit(self):
        token = await self.get_jwt()

        if token is not None:
            self.user_id: int = await self.api.get_id_from_email(
                token, await self.get_email()
            )

        return self

    async def get_user_metadata(self) -> tuple | None:
        user_metadata = await self.db.get_value(key=str(self.tg_id))

        if user_metadata is None:
            return None
        else:
            date, jwt, email = user_metadata.decode("utf-8").split(",")

            return date, jwt, email

    @property
    async def role(self) -> str:
        role: str = await self.api.get_user_role(await self.get_jwt(), self.user_id)

        return role

    async def get_jwt(self) -> str | None:
        now = time.time()
        user_metadata = await self.get_user_metadata()

        if user_metadata is None:
            return None
        else:
            date, jwt, _ = user_metadata

            if now - int(date) > 3600:
                await self.db.del_value(key=str(self.tg_id))
                return None

            return jwt

    async def get_email(self) -> str | None:
        if self.__email is None:
            user_metadata = await self.get_user_metadata()

            if user_metadata is None:
                return None
            else:
                _, _, email = user_metadata

                return email
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
