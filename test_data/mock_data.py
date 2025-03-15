import random
import datetime


def get_homepage_mock_data(user_id: str) -> dict:
    if user_id != "205159314":
        return {"error": f"No data for user_id={user_id}"}
    default_bot_users = 47000
    default_bot = {
        "bot_id": 100,
        "bot_link": "@main_bot",
        "total_users": default_bot_users,
        "mirror": False,
        "mirrors": [{"bot_id": 200, "bot_link": "@main_bot_mirror", "total_users": 12300, "mirror": True}],
        "user_stats": {"users": _get_users_mock(bot_id=100, user_type="all", interval="week")},
        "message_stats": {"messages": _get_messages_mock(bot_id=100, msg_type="all", interval="week")},
    }
    return {
        "default_bot": default_bot,
        "bot_list": [
            {
                "bot_id": 100,
                "bot_link": "@main_bot",
                "total_users": 47000,
                "mirror": False,
                "mirrors": [{"bot_id": 200, "bot_link": "@main_bot_mirror", "total_users": 12300, "mirror": True}],
            },
            {
                "bot_id": 200,
                "bot_link": "@main_bot_mirror",
                "total_users": 12300,
                "mirror": True,
                "mirrors": [],
            },
            {
                "bot_id": 300,
                "bot_link": "@another_bot",
                "total_users": 6500,
                "mirror": False,
                "mirrors": [],
            },
        ],
        "mirrors": default_bot.get("mirrors", []),
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
        {
            "bot_id": 200,
            "bot_link": "@main_bot_mirror",
            "total_users": 12300,
            "mirror": True,
            "mirrors": [],
        },
        {
            "bot_id": 300,
            "bot_link": "@another_bot",
            "total_users": 6500,
            "mirror": False,
            "mirrors": [],
        },
    ]
    return {"selected_bot": selected_bot, "bot_list": bot_list}


def get_users_mock_data(bot_id: int, user_type: str, interval: str, mirror: bool) -> dict:
    return _get_users_mock(bot_id, user_type, interval)


def get_messages_mock_data(bot_id: int, msg_type: str, interval: str) -> dict:
    return _get_messages_mock(bot_id, msg_type, interval)


def _get_users_mock(bot_id: int, user_type: str, interval: str) -> dict:
    random.seed(bot_id * 123 + len(user_type) + len(interval))
    if interval == "day":
        data_list = []
        max_base = 50000 if bot_id == 100 else 15000
        now = datetime.datetime.now()
        for i in range(24):
            hour_dt = now - datetime.timedelta(hours=23 - i)
            total = random.randint(0, max_base)
            active = int(total * random.uniform(0.0, 1.0))
            inactive = total - active
            if user_type == "active":
                active = int(total * random.uniform(0.8, 1.0))
                inactive = total - active
            elif user_type == "inactive":
                inactive = int(total * random.uniform(0.7, 1.0))
                active = total - inactive
            data_list.append({"hour": hour_dt.isoformat(), "total": total, "active": active, "inactive": inactive})
        data_list.sort(key=lambda x: x["hour"])
        return {"users": data_list}
    else:
        data_list = []
        max_base = 30000 if bot_id == 100 else 10000
        today = datetime.date.today()
        for i in range(7):
            date_i = today - datetime.timedelta(days=6 - i)
            total = random.randint(0, max_base)
            active = int(total * random.uniform(0.0, 1.0))
            inactive = total - active
            if user_type == "active":
                active = int(total * random.uniform(0.8, 1.0))
                inactive = total - active
            elif user_type == "inactive":
                inactive = int(total * random.uniform(0.7, 1.0))
                active = total - inactive
            data_list.append({"date": str(date_i), "total": total, "active": active, "inactive": inactive})
        return {"users": data_list}


def _get_messages_mock(bot_id: int, msg_type: str, interval: str) -> dict:
    random.seed(bot_id * 999 + len(msg_type) + len(interval))
    if interval == "day":
        data_list = []
        max_base = 20000 if bot_id == 100 else 7000
        now = datetime.datetime.now()
        for i in range(24):
            hour_dt = now - datetime.timedelta(hours=23 - i)
            greetings = random.randint(0, max_base)
            goodbyes = random.randint(0, int(max_base * 0.5))
            mail_active = random.randint(0, 300)
            mail_inactive = random.randint(0, 200)
            data_list.append(
                {
                    "hour": hour_dt.isoformat(),
                    "greetings": greetings,
                    "goodbyes": goodbyes,
                    "mailings": {"active": mail_active, "inactive": mail_inactive, "count": random.randint(1, 5)},
                }
            )
            data_list.sort(key=lambda x: x["hour"])
        return {"messages": data_list}
    else:
        data_list = []
        max_base = 18000 if bot_id == 100 else 5000
        today = datetime.date.today()
        for i in range(7):
            date_i = today - datetime.timedelta(days=6 - i)
            greetings = random.randint(0, max_base)
            goodbyes = random.randint(0, int(max_base * 0.4))
            mail_active = random.randint(0, 300)
            mail_inactive = random.randint(0, 200)
            data_list.append(
                {
                    "date": str(date_i),
                    "greetings": greetings,
                    "goodbyes": goodbyes,
                    "mailings": {"active": mail_active, "inactive": mail_inactive, "count": random.randint(1, 5)},
                }
            )
        return {"messages": data_list}
