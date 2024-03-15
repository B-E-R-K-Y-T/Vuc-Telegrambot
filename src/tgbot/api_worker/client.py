import json
from copy import copy
from http import HTTPStatus

from tgbot.api_worker.request import Request


class APIWorker:
    def __init__(self):
        self.request = Request()
        self.headers = {
            "accept": "application/json",
        }

    async def login(self, username: str, password: str) -> str | None:
        """
        Вернет JWT токен в виде строки
        """
        self.headers["Content-Type"] = "application/x-www-form-urlencoded"

        data = {"username": username, "password": password}

        resp = await self.request.post(
            "/auth/jwt/login", headers=self.headers, data=data
        )

        if resp is None:
            return None

        if resp.status == HTTPStatus.NO_CONTENT.value:
            token = resp.cookies.get("bonds").value
            # del self.headers['Content-Type']
            #
            # await self.request.patch('/users/set_user_attr',
            #                          headers=self.headers,
            #                          data={'telegram_id': telegram_id},
            #                          cookies={'bonds': token})

            return token

    async def logout(self, token: str) -> bool:
        resp = await self.request.post(
            "/auth/jwt/logout", headers=self.headers, cookies={"bonds": token}
        )

        if resp.status == HTTPStatus.NO_CONTENT.value:
            return True

        return False

    async def get_id_from_tg(self, token: str, telegram_id: int) -> int:
        resp = await self.request.get(
            "/users/get_id_from_tg",
            headers=self.headers,
            cookies={"bonds": token},
            params={"telegram_id": telegram_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return (await resp.json())["id"]

    async def get_id_from_email(self, token: str, email: str) -> int:
        resp = await self.request.get(
            "/users/get_id_from_email",
            headers=self.headers,
            cookies={"bonds": token},
            params={"email": email},
        )

        if resp.status == HTTPStatus.OK.value:
            return (await resp.json())["id"]

    async def get_user_role(self, token: str, user_id: int) -> str:
        resp = await self.request.get(
            "/users/get_user_role",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return (await resp.json())["role"]

    async def get_self(self, token: str, user_id: int) -> str:
        resp = await self.request.get(
            "/users/get_self",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_semesters(self, token: str, user_id: int) -> list[int]:
        resp = await self.request.get(
            "/professor/get_semesters",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return [int(sem) for sem in (await resp.json())["semesters"]]

    async def get_attend(self, token: str, user_id: int) -> list[int]:
        resp = await self.request.get(
            "/users/get_attendance_status_user",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def set_user_attr(self, token: str, attrs: dict) -> str:
        headers = copy(self.headers)

        headers['accept'] = '*/*'
        headers['Content-Type'] = 'application/json'

        resp = await self.request.patch(
            "/users/set_user_attr",
            headers=headers,
            cookies={"bonds": token},
            data=json.dumps(attrs),
        )

        return resp


__all__ = (
    APIWorker.__name__,
)
