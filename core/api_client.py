from urllib.parse import urljoin

import aiohttp
from typing import Any

from aiohttp import ClientTimeout

from core.logger import logger
from core.settings import Settings


class APIClient:
    _session: aiohttp.ClientSession | None = None
    API_TIMEOUT = ClientTimeout(total=Settings.API_TIMEOUT)

    @classmethod
    async def _get_session(cls) -> aiohttp.ClientSession:
        if cls._session is None or cls._session.closed:
            cls._session = aiohttp.ClientSession(timeout=cls.API_TIMEOUT)
        return cls._session

    @classmethod
    async def _make_request(
        cls, method: str, endpoint: str, params: dict | None = None, headers: dict | None = None
    ) -> dict[str, Any]:
        url = urljoin(Settings.WEBHOOK_HOST, endpoint)
        session = await cls._get_session()
        logger.debug(f"Making {method} request to {url} with params {params} and headers {headers}")

        try:
            async with session.request(method, url, params=params, headers=headers) as response:
                data = await response.json()
                logger.info(f"Response {response.status} from {url}: {data}")
                return data

        except aiohttp.ClientError as e:
            logger.error(f"Error making {method} request to {url}: {e}")
            return {"error": str(e)}

    @classmethod
    async def get_user_homepage(cls, user_id: str) -> dict[str, Any]:
        endpoint = f"/start/{user_id}"
        return await cls._make_request("GET", endpoint)

    @classmethod
    async def close(cls) -> None:
        if cls._session and not cls._session.closed:
            await cls._session.close()
