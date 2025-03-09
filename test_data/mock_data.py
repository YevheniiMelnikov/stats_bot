import random
import datetime


def get_users_mock_data(bot_id: int, user_type: str, interval: str, mirror: bool) -> dict:
    seed_str = f"{bot_id}-{user_type}-{interval}-mirror={mirror}"
    random.seed(seed_str)
    base_mult = (bot_id % 100) + 1
    mirror_factor = 0.7 if mirror else 1.0

    if interval == "day":
        hours = random.sample(range(0, 24), k=3)
        hours.sort()
        data = []
        for h in hours:
            total = int(random.randint(50, 120) * base_mult * mirror_factor)
            active = int(total * random.uniform(0.5, 0.9))
            inactive = total - active

            if user_type == "active":
                active = int(total * random.uniform(0.8, 0.95))
                inactive = total - active
            elif user_type == "inactive":
                inactive = int(total * random.uniform(0.5, 0.8))
                active = total - inactive

            data.append({"hour": h, "total": total, "active": active, "inactive": inactive})
        return {"users": data}

    else:
        days_count = random.randint(5, 7)
        today = datetime.date.today()
        data = []
        for i in range(days_count):
            date_i = today - datetime.timedelta(days=i)
            total = int(random.randint(50, 120) * base_mult * mirror_factor)
            active = int(total * random.uniform(0.5, 0.9))
            inactive = total - active

            if user_type == "active":
                active = int(total * random.uniform(0.8, 0.95))
                inactive = total - active
            elif user_type == "inactive":
                inactive = int(total * random.uniform(0.5, 0.8))
                active = total - inactive

            data.append({"date": str(date_i), "total": total, "active": active, "inactive": inactive})

        data.sort(key=lambda x: x["date"])
        return {"users": data}


def get_messages_mock_data(bot_id: int, msg_type: str, interval: str) -> dict:
    seed_str = f"{bot_id}-{msg_type}-{interval}"
    random.seed(seed_str)

    base_mult = (bot_id % 50) + 1
    if msg_type == "greetings":
        type_factor = 1.2
    elif msg_type == "goodbyes":
        type_factor = 0.8
    elif msg_type == "mailings":
        type_factor = 1.0
    else:
        type_factor = 0.9

    if interval == "day":
        points_count = random.randint(2, 4)
        data = []
        hours = random.sample(range(0, 24), k=points_count)
        hours.sort()
        for h in hours:
            greetings = int(random.randint(1, 50) * base_mult * type_factor)
            goodbyes = int(greetings * random.uniform(0.3, 0.7))
            mailings_active = int(random.randint(0, 20) * base_mult * 0.2)
            mailings_inactive = int(random.randint(0, 10) * base_mult * 0.2)
            total = greetings + goodbyes + mailings_active + mailings_inactive

            data.append(
                {
                    "hour": h,
                    "greetings": greetings,
                    "goodbyes": goodbyes,
                    "mailings": {"active": mailings_active, "inactive": mailings_inactive},
                    "total": total,
                }
            )
        return {"messages": data}
    else:
        days_count = random.randint(5, 7)
        today = datetime.date.today()
        data = []
        for i in range(days_count):
            date_i = today - datetime.timedelta(days=i)

            greetings = int(random.randint(10, 100) * base_mult * type_factor)
            goodbyes = int(greetings * random.uniform(0.3, 0.8))
            mailings_active = int(random.randint(0, 30) * base_mult * 0.3)
            mailings_inactive = int(random.randint(0, 30) * base_mult * 0.2)
            total = greetings + goodbyes + mailings_active + mailings_inactive

            data.append(
                {
                    "date": str(date_i),
                    "greetings": greetings,
                    "goodbyes": goodbyes,
                    "mailings": {"active": mailings_active, "inactive": mailings_inactive},
                    "total": total,
                }
            )
        data.sort(key=lambda x: x["date"])
        return {"messages": data}


def get_homepage_mock_data(user_id: str) -> dict:
    base_mult = (int(user_id) % 500) + 1
    default_bot_users = 20000 + 50 * base_mult

    return {
        "default_bot": {
            "bot_id": 123,
            "bot_link": "@some_bot",
            "total_users": default_bot_users,
            "mirror": False,
            "mirrors": [],
            "user_stats": {
                "users": [
                    {
                        "hour": 11,
                        "total": default_bot_users,
                        "active": int(default_bot_users * 0.75),
                        "inactive": int(default_bot_users * 0.25),
                    }
                ]
            },
            "message_stats": {
                "messages": [
                    {"hour": 11, "greetings": 50, "goodbyes": 20, "mailings": {"active": 5, "inactive": 3}, "total": 78}
                ]
            },
        },
        "bot_list": [
            {"bot_id": 123, "bot_link": "@some_bot", "total_users": default_bot_users, "mirror": False, "mirrors": []},
            {"bot_id": 200, "bot_link": "@another_bot", "total_users": 8500, "mirror": False, "mirrors": []},
        ],
    }


def get_selected_bot_mock_data(bot_id: int) -> dict:
    seed_str = f"{bot_id}-selected-bot"
    random.seed(seed_str)

    base_mult = (bot_id % 300) + 50
    total_users = int(base_mult * 100)

    if bot_id == 200:
        selected_bot = {
            "bot_id": 200,
            "bot_link": "@another_bot",
            "total_users": 8500,
            "mirror": False,
            "mirrors": [],
            "user_stats": {
                "users": [
                    {"hour": 11, "total": 50, "active": 35, "inactive": 15},
                    {"hour": 12, "total": 80, "active": 60, "inactive": 20},
                ]
            },
            "message_stats": {
                "messages": [
                    {"hour": 11, "greetings": 10, "goodbyes": 5, "mailings": {"active": 2, "inactive": 1}, "total": 18},
                    {"hour": 12, "greetings": 20, "goodbyes": 5, "mailings": {"active": 5, "inactive": 2}, "total": 32},
                ]
            },
        }
    else:
        hours = random.sample(range(0, 24), k=2)
        hours.sort()
        user_data = []
        msg_data = []
        for h in hours:
            t = random.randint(50, 150)
            active = int(t * random.uniform(0.6, 0.9))
            inactive = t - active

            g = random.randint(10, 60)
            gb = int(g * random.uniform(0.3, 0.8))
            ma = random.randint(0, 10)
            mi = random.randint(0, 10)
            msg_total = g + gb + ma + mi

            user_data.append({"hour": h, "total": t, "active": active, "inactive": inactive})
            msg_data.append(
                {
                    "hour": h,
                    "greetings": g,
                    "goodbyes": gb,
                    "mailings": {"active": ma, "inactive": mi},
                    "total": msg_total,
                }
            )

        selected_bot = {
            "bot_id": bot_id,
            "bot_link": f"@unknown_bot_{bot_id}",
            "total_users": total_users,
            "mirror": False,
            "mirrors": [],
            "user_stats": {"users": user_data},
            "message_stats": {"messages": msg_data},
        }

    bot_list = [
        {"bot_id": 123, "bot_link": "@some_bot", "total_users": 30000, "mirror": False, "mirrors": []},
        {"bot_id": 200, "bot_link": "@another_bot", "total_users": 8500, "mirror": False, "mirrors": []},
        {"bot_id": 777, "bot_link": "@bot777", "total_users": 7777, "mirror": False, "mirrors": []},
        {
            "bot_id": bot_id,
            "bot_link": f"@dynamic_{bot_id}",
            "total_users": total_users,
            "mirror": False,
            "mirrors": [],
        },
    ]

    return {"selected_bot": selected_bot, "bot_list": bot_list}
