import os
from dataclasses import dataclass


@dataclass
class Settings:
    BOT_TOKEN: str = os.getenv("BOT_TOKEN")
    REDIS_URL: str = os.getenv("REDIS_URL")
    HEALTHCHECK_INTERVAL: int = 60 * 5


settings = Settings()
