import asyncio

from core.logger import logger
from core.settings import settings


async def run():
    while True:
        logger.info("Health check")
        await asyncio.sleep(settings.HEALTHCHECK_INTERVAL)
