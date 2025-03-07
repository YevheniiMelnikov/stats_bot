from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class BotInfo:
    bot_id: int
    bot_link: str
    owner_id: int
    total_users: int
    mirror: bool = False
    mirrors: list[BotInfo] | None = None


@dataclass
class UserStatRecord:
    from_time: datetime
    to_time: datetime
    active: int
    inactive: int
    total: int


@dataclass
class MessageStatRecord:
    from_time: datetime
    to_time: datetime
    greetings: int
    farewells: int
    mailings: int
    total: int
