from __future__ import annotations
from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class BotInfo:
    bot_id: int
    bot_link: str
    total_users: int
    registered_at: datetime
    mirror: bool = False
    mirrors: list[BotInfo] | None = None


@dataclass
class UserStatRecord:
    time: date | str
    active: int
    inactive: int
    total: int


@dataclass
class MessageStatRecord:
    time: date | str
    greetings: int
    goodbyes: int
    mailings: int
    total: int
