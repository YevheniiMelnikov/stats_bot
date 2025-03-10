import random
import datetime


def get_homepage_mock_data(user_id: str) -> dict:
    if user_id != "205159314":
        return {"error": f"No data for user_id={user_id}"}

    default_bot_users = 47000
    return {
        "default_bot": {
            "bot_id": 100,
            "bot_link": "@main_bot",
            "total_users": default_bot_users,
            "mirror": False,
            "mirrors": [{"bot_id": 200, "bot_link": "@main_bot_mirror", "total_users": 12300, "mirror": True}],
            "user_stats": {"users": _get_users_mock(bot_id=100, user_type="all", interval="week")},
            "message_stats": {"messages": _get_messages_mock(bot_id=100, msg_type="all", interval="week")},
        },
        "bot_list": [
            {
                "bot_id": 100,
                "bot_link": "@main_bot",
                "total_users": 47000,
                "mirror": False,
                "mirrors": [{"bot_id": 200, "bot_link": "@main_bot_mirror", "total_users": 12300, "mirror": True}],
            },
            {"bot_id": 200, "bot_link": "@main_bot_mirror", "total_users": 12300, "mirror": True, "mirrors": []},
            {"bot_id": 300, "bot_link": "@another_bot", "total_users": 6500, "mirror": False, "mirrors": []},
        ],
    }


def get_selected_bot_mock_data(bot_id: int) -> dict:
    if bot_id == 100:
        selected_bot = {
            "bot_id": 100,
            "bot_link": "@main_bot",
            "total_users": 47000,
            "mirror": False,
            "mirrors": [{"bot_id": 200, "bot_link": "@main_bot_mirror", "total_users": 12300, "mirror": True}],
            "user_stats": {"users": _get_users_mock(bot_id=100, user_type="all", interval="week")["users"]},
            "message_stats": {"messages": _get_messages_mock(bot_id=100, msg_type="all", interval="week")["messages"]},
        }
    elif bot_id == 200:
        selected_bot = {
            "bot_id": 200,
            "bot_link": "@main_bot_mirror",
            "total_users": 12300,
            "mirror": True,
            "mirrors": [],
            "user_stats": {"users": _get_users_mock(bot_id=200, user_type="all", interval="week")["users"]},
            "message_stats": {"messages": _get_messages_mock(bot_id=200, msg_type="all", interval="week")["messages"]},
        }
    elif bot_id == 300:
        selected_bot = {
            "bot_id": 300,
            "bot_link": "@another_bot",
            "total_users": 6500,
            "mirror": False,
            "mirrors": [],
            "user_stats": {"users": _get_users_mock(bot_id=300, user_type="all", interval="week")["users"]},
            "message_stats": {"messages": _get_messages_mock(bot_id=300, msg_type="all", interval="week")["messages"]},
        }
    else:
        return {"error": f"No data for bot_id={bot_id}"}

    bot_list = [
        {
            "bot_id": 100,
            "bot_link": "@main_bot",
            "total_users": 47000,
            "mirror": False,
            "mirrors": [{"bot_id": 200, "bot_link": "@main_bot_mirror", "total_users": 12300, "mirror": True}],
        },
        {"bot_id": 200, "bot_link": "@main_bot_mirror", "total_users": 12300, "mirror": True, "mirrors": []},
        {"bot_id": 300, "bot_link": "@another_bot", "total_users": 6500, "mirror": False, "mirrors": []},
    ]
    return {"selected_bot": selected_bot, "bot_list": bot_list}


def get_users_mock_data(bot_id: int, user_type: str, interval: str, mirror: bool) -> dict:
    data = _get_users_mock(bot_id, user_type, interval)
    return data


def get_messages_mock_data(bot_id: int, msg_type: str, interval: str) -> dict:
    data = _get_messages_mock(bot_id, msg_type, interval)
    return data


def _get_users_mock(bot_id: int, user_type: str, interval: str) -> dict:
    random.seed(bot_id * 123 + len(user_type) + len(interval))

    if interval == "day":
        data_list = []
        base_num = 20000 if bot_id == 100 else 5000
        now = datetime.datetime.now()
        for i in range(24):
            hour_dt = now - datetime.timedelta(hours=23 - i)
            total = base_num + random.randint(0, 300)
            active = int(total * random.uniform(0.7, 0.9))
            inactive = total - active
            if user_type == "active":
                active = int(total * 0.95)
                inactive = total - active
            elif user_type == "inactive":
                inactive = int(total * 0.7)
                active = total - inactive

            data_list.append({"hour": hour_dt.hour, "total": total, "active": active, "inactive": inactive})
        return {"users": data_list}
    else:
        data_list = []
        base_num = 20000 if bot_id == 100 else 5000
        today = datetime.date.today()
        for i in range(7):
            date_i = today - datetime.timedelta(days=6 - i)
            total = base_num + random.randint(0, 2000)
            active = int(total * random.uniform(0.6, 0.85))
            inactive = total - active
            if user_type == "active":
                active = int(total * 0.9)
                inactive = total - active
            elif user_type == "inactive":
                inactive = int(total * 0.6)
                active = total - inactive

            data_list.append({"date": str(date_i), "total": total, "active": active, "inactive": inactive})
        return {"users": data_list}


def _get_messages_mock(bot_id: int, msg_type: str, interval: str) -> dict:
    random.seed(bot_id * 999 + len(msg_type) + len(interval))

    if interval == "day":
        data_list = []
        base_num = 5000 if bot_id == 100 else 1000
        now = datetime.datetime.now()
        for i in range(24):
            hour_dt = now - datetime.timedelta(hours=23 - i)
            greetings = base_num + random.randint(0, 200)
            goodbyes = int(greetings * random.uniform(0.1, 0.3))
            mailings_active = random.randint(10, 100)
            mailings_inactive = random.randint(10, 50)

            data_list.append(
                {
                    "hour": hour_dt.hour,
                    "greetings": greetings,
                    "goodbyes": goodbyes,
                    "mailings": {"active": mailings_active, "inactive": mailings_inactive},
                }
            )
        return {"messages": data_list}
    else:
        data_list = []
        base_num = 5000 if bot_id == 100 else 1000
        today = datetime.date.today()
        for i in range(7):
            date_i = today - datetime.timedelta(days=6 - i)
            greetings = base_num + random.randint(100, 500)
            goodbyes = int(greetings * random.uniform(0.2, 0.5))
            mailings_active = random.randint(100, 300)
            mailings_inactive = random.randint(50, 150)

            data_list.append(
                {
                    "date": str(date_i),
                    "greetings": greetings,
                    "goodbyes": goodbyes,
                    "mailings": {"active": mailings_active, "inactive": mailings_inactive},
                }
            )
        return {"messages": data_list}
