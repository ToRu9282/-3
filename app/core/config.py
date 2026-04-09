import os
from dataclasses import dataclass

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    database_url: str
    cors_origins: list[str]


def get_settings() -> Settings:
    load_dotenv()
    db_url = os.getenv("DATABASE_URL")
    cors_origin = os.getenv(
        "CORS_ORIGINS", "http://localhost:3000"
    )  # значение по умолчанию

    # Проверка на None для обязательной переменной
    if db_url is None:
        raise ValueError("DATABASE_URL environment variable is not set")

    return Settings(
        database_url=db_url,
        cors_origins=[cors_origin],  # заворачиваем в список
    )
