import os
from dataclasses import dataclass


@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    REDIS_URL: str = os.getenv("REDIS_URL")
    WEB_SERVER_HOST: str = os.getenv("WEB_SERVER_HOST")
    WEBHOOK_PORT: int = int(os.getenv("WEBHOOK_PORT"))
    WEBHOOK_HOST: str = os.getenv("WEBHOOK_HOST")
    WEBHOOK_PATH: str = "/statistics"
    WEBHOOK_URL: str = f"{WEBHOOK_HOST}{WEBHOOK_PATH}"


settings = Settings()
