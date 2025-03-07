from urllib.parse import urljoin

import aiohttp
from typing import Any

from aiohttp import ClientTimeout

from core.logger import logger
from core.settings import Settings


class APIClient:
    API_TIMEOUT = ClientTimeout(total=Settings.API_TIMEOUT)

    @classmethod
    async def _make_request(cls, method: str, endpoint: str, params: dict | None = None) -> dict[str, Any]:
        url = urljoin(Settings.WEBHOOK_HOST, endpoint)
        logger.debug(f"Making {method} request to {url}")
        async with aiohttp.ClientSession(timeout=cls.API_TIMEOUT) as session:
            try:
                async with session.request(method, url, params=params) as response:
                    data = await response.json()
                    return data
            except aiohttp.ClientError as e:
                logger.error(f"Error making {method} request to {url}: {e}")
                return {"error": str(e)}

    @classmethod
    async def get_bot_list(cls, user_id: int) -> dict[str, Any]:
        endpoint = f"/api/users/{user_id}"
        return await cls._make_request("GET", endpoint)

    @classmethod
    async def get_bot_stats(cls, bot_id: int) -> dict[str, Any]:
        endpoint = f"/api/bots/{bot_id}"
        return await cls._make_request("GET", endpoint)

    # Response examples:

    # get_bot_list

    # {
    #     "bots": [
    #         {
    #             "bot_id": 123,
    #             "bot_link": "https://t.me/some_bot",
    #             "owner_id": 42,
    #             "total_users": 1000,
    #             "mirror": false,
    #             "mirrors": [
    #                 {
    #                     "bot_id": 789,
    #                     "bot_link": "https://t.me/some_bot_mirror",
    #                     "owner_id": 42,
    #                     "total_users": 300,
    #                     "mirror": true
    #                 }
    #             ]
    #         },
    #         {
    #             "bot_id": 456,
    #             "bot_link": "https://t.me/another_bot",
    #             "owner_id": 42,
    #             "total_users": 200,
    #             "mirror": false,
    #             "mirrors": []
    #         }
    #     ]
    # }

    # get_bot_stats

    #   {
    #     "users_stats": {
    #         "daily": [
    #             {
    #                 "from_time": "2025-03-07T00:00:00Z",
    #                 "to_time": "2025-03-07T01:00:00Z",
    #                 "active": 5,
    #                 "inactive": 2,
    #                 "total": 7
    #             },
    #             {
    #                 "from_time": "2025-03-07T01:00:00Z",
    #                 "to_time": "2025-03-07T02:00:00Z",
    #                 "active": 3,
    #                 "inactive": 4,
    #                 "total": 7
    #             },
    #             {
    #                 "from_time": "2025-03-07T02:00:00Z",
    #                 "to_time": "2025-03-07T03:00:00Z",
    #                 "active": 10,
    #                 "inactive": 2,
    #                 "total": 12
    #             }
    #         ],
    #         "weekly": [
    #             {
    #                 "from_time": "2025-03-01T00:00:00Z",
    #                 "to_time": "2025-03-02T00:00:00Z",
    #                 "active": 50,
    #                 "inactive": 20,
    #                 "total": 70
    #             },
    #             {
    #                 "from_time": "2025-03-02T00:00:00Z",
    #                 "to_time": "2025-03-03T00:00:00Z",
    #                 "active": 30,
    #                 "inactive": 40,
    #                 "total": 70
    #             },
    #             {
    #                 "from_time": "2025-03-03T00:00:00Z",
    #                 "to_time": "2025-03-04T00:00:00Z",
    #                 "active": 100,
    #                 "inactive": 20,
    #                 "total": 120
    #             }
    #         ]
    #     },
    #     "messages_stats": {
    #         "daily": [
    #             {
    #                 "from_time": "2025-03-07T00:00:00Z",
    #                 "to_time": "2025-03-07T01:00:00Z",
    #                 "greetings": 10,
    #                 "farewells": 5,
    #                 "mailings": 2,
    #                 "total": 17
    #             },
    #             {
    #                 "from_time": "2025-03-07T01:00:00Z",
    #                 "to_time": "2025-03-07T02:00:00Z",
    #                 "greetings": 7,
    #                 "farewells": 2,
    #                 "mailings": 1,
    #                 "total": 10
    #             },
    #             {
    #                 "from_time": "2025-03-07T02:00:00Z",
    #                 "to_time": "2025-03-07T03:00:00Z",
    #                 "greetings": 8,
    #                 "farewells": 1,
    #                 "mailings": 3,
    #                 "total": 12
    #             }
    #         ],
    #         "weekly": [
    #             {
    #                 "from_time": "2025-03-01T00:00:00Z",
    #                 "to_time": "2025-03-02T00:00:00Z",
    #                 "greetings": 100,
    #                 "farewells": 50,
    #                 "mailings": 20,
    #                 "total": 170
    #             },
    #             {
    #                 "from_time": "2025-03-02T00:00:00Z",
    #                 "to_time": "2025-03-03T00:00:00Z",
    #                 "greetings": 70,
    #                 "farewells": 20,
    #                 "mailings": 10,
    #                 "total": 100
    #             },
    #             {
    #                 "from_time": "2025-03-03T00:00:00Z",
    #                 "to_time": "2025-03-04T00:00:00Z",
    #                 "greetings": 80,
    #                 "farewells": 10,
    #                 "mailings": 30,
    #                 "total": 120
    #             }
    #         ]
    #     }
    # }
