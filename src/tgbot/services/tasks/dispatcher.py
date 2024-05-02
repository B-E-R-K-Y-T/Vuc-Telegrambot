from typing import Optional

from aiohttp import web
from aiohttp.abc import Request

from config import app_settings
from tgbot.services.api_worker.server import HttpServer
from tgbot.services.tasks.auth import authenticate
from tgbot.services.tasks.handlers import handlers_collector
from tgbot.services.tasks.types import TaskTypes, StatusTask

task_server = HttpServer(
    host=app_settings.TASK_WORKER_HOST, port=app_settings.TASK_WORKER_PORT
)


@task_server.post(endpoint="/tasks")
@authenticate
async def task_dispatcher(request: Request):
    data = await request.json()
    status_task: Optional[dict] = None

    if data["type"] == TaskTypes.SEND_USER_MESSAGE:
        status_task = await handlers_collector.start(
            TaskTypes.SEND_USER_MESSAGE,
            telegram_id=data["telegram_id"],
            message=data["message"],
        )
    elif data["type"] == TaskTypes.SEND_PLATOON_MESSAGE:
        status_task = await handlers_collector.start(
            TaskTypes.SEND_PLATOON_MESSAGE,
            users_tg=data["users_tg"],
            message=data["message"],
        )
    elif data["type"] == TaskTypes.ANSWER_ATTEND:
        status_task = await handlers_collector.start(
            TaskTypes.ANSWER_ATTEND,
            telegram_id=data["telegram_id"],
            message=data["message"],
        )

    if status_task is None:
        return web.json_response(
            {"status_task": StatusTask.ERROR, "message": "Unknown task type"}
        )

    return web.json_response(status_task)
