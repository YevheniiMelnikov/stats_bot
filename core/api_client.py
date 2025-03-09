import aiohttp
from aiohttp import ClientTimeout
from urllib.parse import urljoin
from typing import Any
from core.settings import Settings
from core.logger import logger


class APIClient:
    _session: aiohttp.ClientSession | None = None
    API_TIMEOUT = ClientTimeout(total=Settings.API_TIMEOUT)

    @classmethod
    async def _get_session(cls) -> aiohttp.ClientSession:
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession(timeout=cls.API_TIMEOUT)
        return cls._session

    @classmethod
    async def close(cls) -> None:
        if cls._session and not cls._session.closed:
            await cls._session.close()

    @classmethod
    async def _make_request(
        cls, method: str, endpoint: str, params: dict[str, Any] | None = None, headers: dict | None = None
    ) -> dict[str, Any]:
        url = urljoin(Settings.WEBHOOK_HOST, endpoint)
        session = await cls._get_session()
        logger.debug(f"Making {method} request to {url} with params={params} and headers={headers}")
        try:
            async with session.request(method, url, params=params, headers=headers) as response:
                data = await response.json()
                return data
        except aiohttp.ClientError as e:
            logger.error(f"Error making {method} request to {url}: {e}")
            return {"error": str(e)}

    @classmethod
    async def get_user_homepage(cls, user_id: str) -> dict[str, Any]:
        params = {"action": "start", "user_id": user_id}
        return await cls._make_request("GET", "/stats", params=params)

    @classmethod
    async def get_bot_data(cls, bot_id: int) -> dict[str, Any]:
        params = {"action": "bot", "bot_id": bot_id}
        return await cls._make_request("GET", "/stats", params=params)

    @classmethod
    async def get_users_data(cls, bot_id: int, user_type: str, interval: str, mirror: bool = False) -> dict[str, Any]:
        params = {
            "action": "users",
            "bot_id": bot_id,
            "type": user_type,
            "interval": interval,
            "mirror": "true" if mirror else "false",
        }
        return await cls._make_request("GET", "/stats", params=params)

    @classmethod
    async def get_messages_data(cls, bot_id: int, msg_type: str, interval: str) -> dict[str, Any]:
        params = {"action": "messages", "bot_id": bot_id, "type": msg_type, "interval": interval}
        return await cls._make_request("GET", "/stats", params=params)
