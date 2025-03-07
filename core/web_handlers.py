import json
import os

from aiohttp import web
from aiohttp.web_fileresponse import FileResponse

from core.api_client import APIClient
import plotly.graph_objects as go
from core.logger import logger
from core.models import UserStatRecord
from core.parser import DataParer


async def webapp_handler(request: web.Request) -> FileResponse:
    file_path = os.path.join(os.path.dirname(__file__), "..", "static", "templates", "index.html")
    return web.FileResponse(file_path)


async def get_stats_handler(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON"}, status=400)

    if not (bot_id := data.get("bot_id")):
        return web.json_response({"error": "bot_id required"}, status=400)

    try:
        client: APIClient = request.app["api_client"]
        result = await client.get_bot_stats(bot_id)
        if "error" not in result:
            logger.debug(f"Statistics for bot {bot_id} successfully fetched")
        return web.json_response(result, status=400 if "error" in result else 200)

    except Exception as e:
        logger.error(f"Handler error: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)


async def get_bots_handler(request: web.Request) -> web.Response:
    try:
        data = await request.json()
    except json.JSONDecodeError:
        return web.json_response({"error": "Invalid JSON"}, status=400)

    if not (user_id := data.get("user_id")):
        return web.json_response({"error": "user_id required"}, status=400)

    try:
        client: APIClient = request.app["api_client"]
        result = await client.get_bot_list(user_id)
        if "error" not in result:
            logger.debug(f"Bots list for user {user_id} successfully fetched")
        return web.json_response(result, status=400 if "error" in result else 200)

    except Exception as e:
        logger.error(f"Handler error: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)


async def generate_graphs_handler(request: web.Request) -> web.Response:  # DRAFT
    try:
        data = await request.json()
        stats = DataParer(data["stats"])
        stats.parse_data()
        fig = go.Figure()

        if isinstance(stats._parsed_data[0], UserStatRecord):  # TODO: ADD PROPERTY TO ACCESS CLASS DATA
            times = [record.from_time for record in stats._parsed_data]
            active = [record.active for record in stats._parsed_data]
            inactive = [record.inactive for record in stats._parsed_data]

            fig.add_trace(go.Scatter(x=times, y=active, name="Active Users"))
            fig.add_trace(go.Scatter(x=times, y=inactive, name="Inactive Users"))
        else:
            times = [record.from_time for record in stats._parsed_data]
            messages = [record.total for record in stats._parsed_data]

            fig.add_trace(go.Scatter(x=times, y=messages, name="Total Messages"))

        graph_html = fig.to_html(full_html=False)
        return web.json_response({"graph_html": graph_html})

    except Exception as e:
        logger.error(f"Error generating graphs: {e}")
        return web.json_response({"error": "Failed to generate graphs"}, status=500)
