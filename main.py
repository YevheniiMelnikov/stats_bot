import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from router import main_router
from core.handlers import webapp_handler, get_stats_handler
from core.logger import logger
from core.settings import settings


async def start_web_app(app: web.Application) -> web.AppRunner:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, settings.WEB_SERVER_HOST, settings.WEBHOOK_PORT)
    await site.start()
    return runner


async def main():
    bot = Bot(token=settings.BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=settings.WEBHOOK_URL)
    dp = Dispatcher(storage=RedisStorage.from_url(settings.REDIS_URL))
    dp.include_router(main_router)

    app = web.Application()
    app["bot"] = bot
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=settings.WEBHOOK_PATH)
    app.router.add_route("*", "/webapp", webapp_handler)
    app.router.add_get("/get_stats", get_stats_handler)
    setup_application(app, dp, bot=bot)
    runner = await start_web_app(app)

    try:
        stop_event = asyncio.Event()
        logger.info("Bot started")
        await stop_event.wait()
    except (KeyboardInterrupt, SystemExit):
        logger.info("Shutting down bot...")
    finally:
        await runner.cleanup()
        dp.shutdown()
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Bot stopped")
