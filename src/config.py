import os

from pydantic_settings import SettingsConfigDict, BaseSettings

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Roles:
    admin = "Admin"
    professor = "Преподаватель"
    platoon_commander = "Командир взвода"
    squad_commander = "Командир отделения"
    student = "Студент"


class AppSettings(BaseSettings):
    TOKEN: str

    MAX_MESSAGES: int
    INTERVAL: float
    TIMEOUT_MESSAGES: int

    SERVER_HOST: str
    SERVER_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    TIME_LIFE_SESSION: int
    TIME_LIFE_CACHE_USERS: int

    MAX_COUNT_MENU_IN_CHAT: int

    TASK_WORKER_HOST: str
    TASK_WORKER_PORT: int

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


app_settings = AppSettings()
