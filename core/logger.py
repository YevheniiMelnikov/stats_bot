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
        {
            "sink": "logs/wabapp_error.log",
            "level": "ERROR",
            "serialize": False,
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            "rotation": "100 MB",
            "retention": "30 days",
            "compression": "zip",
            "enqueue": True,
        },
        {
            "sink": "logs/wabapp_info.log",
            "level": "INFO",
            "serialize": False,
            "format": "{time:YYYY-MM-DD HH:mm:ss} | {level} | {name}:{function}:{line} - {message}",
            "rotation": "100 MB",
            "retention": "30 days",
            "compression": "zip",
            "enqueue": True,
        },
    ]
)
