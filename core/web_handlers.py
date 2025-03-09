import os

from aiohttp import web
from aiohttp.web_fileresponse import FileResponse

from core.api_client import APIClient
import plotly.graph_objects as go
from core.logger import logger
from core.mock_data import (
    get_users_mock_data,
    get_messages_mock_data,
    get_selected_bot_mock_data,
    get_homepage_mock_data,
)
from core.models import UserStatRecord
from core.parser import DataParser


async def webapp_handler(request: web.Request) -> FileResponse:
    file_path = os.path.join(os.path.dirname(__file__), "..", "static", "templates", "index.html")
    return web.FileResponse(file_path)


async def get_homepage_handler(request: web.Request) -> web.Response:
    user_id = request.query.get("user_id")
    if not user_id:
        return web.json_response({"error": "user_id required"}, status=400)

    try:
        client: APIClient = request.app["api_client"]
        result = await client.get_user_homepage(user_id)
        if "error" in result:
            return web.json_response(result, status=400)
        logger.debug(f"Statistics for user {user_id} successfully fetched (default bot)")
        return web.json_response(result, status=200)
    except Exception as e:
        logger.error(f"Handler error in get_homepage_handler: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)


async def get_bot_handler(request: web.Request) -> web.Response:
    bot_id_str = request.match_info.get("bot_id")
    if not bot_id_str:
        return web.json_response({"error": "bot_id required"}, status=400)

    try:
        bot_id = int(bot_id_str)
        client: APIClient = request.app["api_client"]
        result = await client.get_bot_data(bot_id)
        if "error" in result:
            return web.json_response(result, status=400)
        logger.debug(f"Statistics for bot {bot_id} successfully fetched")
        return web.json_response(result, status=200)
    except Exception as e:
        logger.error(f"Handler error in get_bot_handler: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)


async def get_users_handler(request: web.Request) -> web.Response:
    bot_id = request.match_info.get("bot_id")
    users_type = request.match_info.get("type")
    interval = request.match_info.get("interval")
    mirror_str = request.match_info.get("mirror")
    mirror_flag = mirror_str == "true"

    try:
        client: APIClient = request.app["api_client"]
        data = await client.get_users_data(int(bot_id), users_type, interval, mirror=mirror_flag)
        return web.json_response(data)
    except Exception as e:
        logger.error(f"Error in get_users_handler: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)


async def get_messages_handler(request: web.Request) -> web.Response:
    bot_id = request.match_info.get("bot_id")
    msg_type = request.match_info.get("type")
    interval = request.match_info.get("interval")

    try:
        client: APIClient = request.app["api_client"]
        data = await client.get_messages_data(int(bot_id), msg_type, interval)
        return web.json_response(data)
    except Exception as e:
        logger.error(f"Error in get_messages_handler: {e}")
        return web.json_response({"error": "Internal server error"}, status=500)


async def get_stats_handler(request: web.Request) -> web.Response:
    try:
        query = request.query
        action = query.get("action")

        if not action:
            return web.json_response({"error": "Missing 'action'"}, status=400)

        if action == "start":
            user_id = query.get("user_id")
            if not user_id:
                return web.json_response({"error": "Missing 'user_id' for action='start'"}, status=400)
            result = get_homepage_mock_data(user_id)
            return web.json_response(result, status=200)

        elif action == "bot":
            bot_id_str = query.get("bot_id")
            if not bot_id_str:
                return web.json_response({"error": "Missing 'bot_id' for action='bot'"}, status=400)
            bot_id = int(bot_id_str)
            result = get_selected_bot_mock_data(bot_id)
            return web.json_response(result, status=200)

        elif action == "users":
            bot_id_str = query.get("bot_id")
            users_type = query.get("type")
            interval = query.get("interval")
            mirror_str = query.get("mirror", "false")
            mirror_flag = mirror_str == "true"

            if not bot_id_str or not users_type or not interval:
                return web.json_response({"error": "Missing 'bot_id', 'type', or 'interval'"}, status=400)

            result = get_users_mock_data(int(bot_id_str), users_type, interval, mirror_flag)
            return web.json_response(result, status=200)

        elif action == "messages":
            bot_id_str = query.get("bot_id")
            msg_type = query.get("type")
            interval = query.get("interval")

            if not bot_id_str or not msg_type or not interval:
                return web.json_response({"error": "Missing 'bot_id', 'type', or 'interval'"}, status=400)

            result = get_messages_mock_data(int(bot_id_str), msg_type, interval)
            return web.json_response(result, status=200)

        else:
            return web.json_response({"error": f"Unknown action '{action}'"}, status=400)

    except Exception as e:
        logger.error(f"Error in stats_get_handler (action={action}): {e}")
        return web.json_response({"error": "Internal server error"}, status=500)


async def generate_graphs_handler(request: web.Request) -> web.Response:  # DRAFT
    try:
        data = await request.json()
        stats = DataParser(data["stats"])
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
