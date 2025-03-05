import os

from aiohttp import web
from aiohttp.web_fileresponse import FileResponse


async def get_stats_handler(request: web.Request) -> web.Response:
    stats = {"users": 123, "active": 45}
    return web.json_response(stats)


async def webapp_handler(request: web.Request) -> FileResponse:
    file_path = os.path.join(os.path.dirname(__file__), "..", "static", "index.html")
    return web.FileResponse(file_path)
