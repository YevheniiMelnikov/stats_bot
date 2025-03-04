import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from core.logger import logger
from core.settings import settings
from utils import health_check


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    dp = Dispatcher(storage=RedisStorage.from_url(settings.REDIS_URL))
    await bot.delete_webhook(drop_pending_updates=True)
    asyncio.create_task(health_check.run())
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Bot stopped")
