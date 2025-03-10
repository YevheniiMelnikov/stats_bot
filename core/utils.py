from datetime import datetime
from typing import Any
from core.models import UserStatRecord, MessageStatRecord, BotInfo


def convert_user_stats_to_records(data: dict[str, Any]) -> list[UserStatRecord]:
    records = []
    arr = data.get("users", [])
    for item in arr:
        if "hour" in item:
            h = item["hour"]
            dt = datetime.now().replace(hour=h, minute=0, second=0, microsecond=0)
            t = dt
        elif "date" in item:
            d = item["date"]
            t = datetime.fromisoformat(d)
        else:
            continue
        r = UserStatRecord(time=t, active=item["active"], inactive=item["inactive"], total=item["total"])
        records.append(r)
    return records


def convert_messages_to_records(data: dict[str, Any]) -> list[MessageStatRecord]:
    records = []
    arr = data.get("messages", [])
    for item in arr:
        if "hour" in item:
            h = item["hour"]
            dt = datetime.now().replace(hour=h, minute=0, second=0, microsecond=0)
            t = dt
        elif "date" in item:
            d = item["date"]
            t = datetime.fromisoformat(d)
        else:
            continue
        m = item.get("mailings", {})
        if not isinstance(m, dict):
            m = {}
        r = MessageStatRecord(
            time=t, greetings=item["greetings"], goodbyes=item["goodbyes"], mailings=m, total=item["total"]
        )
        records.append(r)
    return records


def convert_dict_to_botinfo(data: dict[str, Any]) -> BotInfo:
    bot_id = data["bot_id"]
    bot_link = data["bot_link"]
    total_users = data["total_users"]
    reg_str = data.get("registered_at")
    if reg_str:
        registered_at = datetime.fromisoformat(reg_str)
    else:
        registered_at = datetime.now()

    mirror = data.get("mirror", False)
    raw_mirrors = data.get("mirrors", [])
    ml = []
    for m in raw_mirrors:
        ml.append(convert_dict_to_botinfo(m))

    return BotInfo(
        bot_id=bot_id,
        bot_link=bot_link,
        total_users=total_users,
        registered_at=registered_at,
        mirror=mirror,
        mirrors=ml,
    )
