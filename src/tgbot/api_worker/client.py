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
            return await resp.json()

    async def get_id_from_email(self, token: str, email: str) -> int:
        resp = await self.request.get(
            "/users/get_id_from_email",
            headers=self.headers,
            cookies={"bonds": token},
            params={"email": email},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_user_role(self, token: str, user_id: int) -> str:
        resp = await self.request.get(
            "/users/get_user_role",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_self(self, token: str, user_id: int) -> dict:
        resp = await self.request.get(
            "/users/get_self",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_user_full_data(self, token: str, user_id: int) -> dict:
        resp = await self.request.get(
            "/users/get_user_full_data",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            result = await resp.json()

            result["id"]

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

    async def get_marks_by_semester(self, token: str, user_id: int, semester: int) -> list[int]:
        resp = await self.request.get(
            "/users/get_marks_by_semester",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id, "semester": semester},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_students_by_squad(self, token: str, platoon_number: int, squad_number: int) -> list[dict]:
        resp = await self.request.get(
            "/squad/get_students_by_squad",
            headers=self.headers,
            cookies={"bonds": token},
            params={"platoon_number": platoon_number, "squad_number": squad_number},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_platoon(self, token: str, platoon_number: int) -> list[dict]:
        resp = await self.request.get(
            "/platoons/get_platoon",
            headers=self.headers,
            cookies={"bonds": token},
            params={"platoon_number": platoon_number},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_count_squad_in_platoon(self, token: str, platoon_number: int) -> int:
        resp = await self.request.get(
            "/platoons/get_count_squad_in_platoon",
            headers=self.headers,
            cookies={"bonds": token},
            params={"platoon_number": platoon_number},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_squad_user(self, token: str, user_id: int) -> int:
        resp = await self.request.get(
            "/users/get_squad_user",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_platoon_number(self, token: str, user_id: int) -> int:
        resp = await self.request.get(
            "/users/get_platoon_user",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_user_name(self, token: str, user_id: int) -> str:
        resp = await self.request.get(
            "/users/get_user_name",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_user_phone(self, token: str, user_id: int) -> int:
        resp = await self.request.get(
            "/users/get_user_phone",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_user_date_of_birth(self, token: str, user_id: int) -> int:
        resp = await self.request.get(
            "/users/get_user_date_of_birth",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_user_institute(self, token: str, user_id: int) -> int:
        resp = await self.request.get(
            "/users/get_user_institute",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_user_address(self, token: str, user_id: int) -> int:
        resp = await self.request.get(
            "/users/get_user_address",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_user_group_study(self, token: str, user_id: int) -> int:
        resp = await self.request.get(
            "/users/get_user_group_study",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def get_user_direction_of_study(self, token: str, user_id: int) -> int:
        resp = await self.request.get(
            "/users/get_user_direction_of_study",
            headers=self.headers,
            cookies={"bonds": token},
            params={"user_id": user_id},
        )

        if resp.status == HTTPStatus.OK.value:
            return await resp.json()

    async def set_user_attr(self, token: str, attrs: dict) -> str:
        headers = copy(self.headers)

        headers["accept"] = "*/*"
        headers["Content-Type"] = "application/json"

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
