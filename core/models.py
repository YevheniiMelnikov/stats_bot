from __future__ import annotations
from dataclasses import dataclass
from datetime import datetime


@dataclass
class UserStatRecord:
    time: datetime
    active: int
    inactive: int
    total: int


@dataclass
class MessageStatRecord:
    time: datetime
    greetings: int
    goodbyes: int
    mailings: dict[str, int]


@dataclass
class BotInfo:
    bot_id: int
    bot_link: str
    total_users: int
    registered_at: datetime
    mirror: bool = False
    mirrors: list[BotInfo] | None = None
