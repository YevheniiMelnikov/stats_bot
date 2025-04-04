import asyncio
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiohttp import web

from core.api_client import APIClient
from core.router import main_router
from core.web_handlers import (
    webapp_handler,
    get_homepage_handler,
    get_users_handler,
    get_messages_handler,
    get_bot_handler,
    get_stats_handler,
    generate_graphs_handler,
)
from core.logger import logger
from core.settings import Settings


async def start_web_app(app: web.Application) -> web.AppRunner:
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, Settings.WEB_SERVER_HOST, Settings.WEBHOOK_PORT)
    await site.start()
    return runner


async def set_app_routes(app: web.Application) -> None:
    app.router.add_route("*", "/webapp", webapp_handler)
    app.router.add_post("/generate_graphs", generate_graphs_handler)
    app.router.add_get("/stats", get_stats_handler)
    app.router.add_get("/home", get_homepage_handler)
    app.router.add_get("/users/{bot_id}/{type}/{interval}", get_users_handler)
    app.router.add_get("/users/{bot_id}/{type}/{interval}/{mirror}", get_users_handler)
    app.router.add_get("/bot/{bot_id}", get_bot_handler)
    app.router.add_get("/messages/{bot_id}/{type}/{interval}", get_messages_handler)
    app.router.add_static("/static/", path="web/static", name="static")


async def shutdown(runner: web.AppRunner, dp: Dispatcher, bot: Bot, api_client: APIClient):
    await runner.cleanup()
    await bot.session.close()
    await api_client.close()
    dp.shutdown()


async def main():
    bot = Bot(token=Settings.BOT_TOKEN)
    await bot.delete_webhook(drop_pending_updates=True)
    await bot.set_webhook(url=Settings.WEBHOOK_URL)
    dp = Dispatcher(storage=RedisStorage.from_url(Settings.REDIS_URL))
    dp.include_router(main_router)

    api_client = APIClient()
    app = web.Application()
    app["bot"] = bot
    app["api_client"] = api_client

    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path=Settings.WEBHOOK_PATH)
    await set_app_routes(app)
    setup_application(app, dp, bot=bot)
    runner = await start_web_app(app)

    try:
        stop_event = asyncio.Event()
        logger.info("Bot started")
        await stop_event.wait()
    except Exception as e:
        logger.critical(f"Bot start failed: {e}")
    finally:
        await shutdown(runner, dp, bot, api_client)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, asyncio.CancelledError):
        logger.info("Bot stopped")
