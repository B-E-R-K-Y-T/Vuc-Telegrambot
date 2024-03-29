import os

from pydantic_settings import SettingsConfigDict, BaseSettings

# Корень проекта
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class AppSettings(BaseSettings):
    TOKEN: str
    MAX_MESSAGES: int
    INTERVAL: int
    TIMEOUT_MESSAGES: int

    SERVER_HOST: str
    SERVER_PORT: int

    REDIS_HOST: str
    REDIS_PORT: int

    model_config = SettingsConfigDict(env_file=f"{BASE_DIR}/.env")


app_settings = AppSettings()
