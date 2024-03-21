from http import HTTPStatus
from typing import Optional

from aiohttp.abc import Request
from aiohttp.web import Response

from config import app_settings
from tgbot.services.api_worker.server import HttpServer
from tgbot.services.tasks.auth import authenticate
from tgbot.services.tasks.handlers import handlers_collector
from tgbot.services.tasks.types import TaskTypes, StatusTask

task_server = HttpServer(
    host=app_settings.TASK_WORKER_HOST,
    port=app_settings.TASK_WORKER_PORT
)


@task_server.post(endpoint="/tasks")
@authenticate
async def task_waiter(request: Request):
    data = await request.json()
    status_task: Optional[StatusTask] = None

    if data["type"] == TaskTypes.SEND_USER_MESSAGE:
        status_task = await handlers_collector.start(
            TaskTypes.SEND_USER_MESSAGE,
            telegram_id=data["telegram_id"],
            message=data["message"]
        )

    if status_task == StatusTask.FINISHED:
        return Response(status=HTTPStatus.OK)

    return Response(status=HTTPStatus.INTERNAL_SERVER_ERROR)
