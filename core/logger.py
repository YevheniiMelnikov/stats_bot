import sys
from loguru import logger

logger.remove()
logger.configure(
    handlers=[
        {
            "sink": sys.stdout,
            "level": "DEBUG",
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",  # noqa
            "colorize": True,
        },
    ]
)
