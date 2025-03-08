from datetime import datetime
from typing import Union

from core.models import UserStatRecord, MessageStatRecord


class DataParser:  # DRAFT
    def __init__(self, raw_data: dict):
        self.raw_data = raw_data
        self._parsed_data: Union[list[UserStatRecord], list[MessageStatRecord]] | None = None

    def parse_data(self) -> None:
        self._parsed_data = []
        for record in self.raw_data.get("stats", []):
            if "active" in record:
                self._parsed_data.append(
                    UserStatRecord(
                        from_time=datetime.fromisoformat(record["from_time"]),
                        to_time=datetime.fromisoformat(record["to_time"]),
                        active=record["active"],
                        inactive=record["inactive"],
                        total=record["total"],
                    )
                )
            elif "greetings" in record:
                self._parsed_data.append(
                    MessageStatRecord(
                        from_time=datetime.fromisoformat(record["from_time"]),
                        to_time=datetime.fromisoformat(record["to_time"]),
                        greetings=record["greetings"],
                        farewells=record["farewells"],
                        mailings=record["mailings"],
                        total=record["total"],
                    )
                )

    def to_json(self) -> dict:
        return {"raw_data": self.raw_data, "has_error": "error" in self.raw_data}


a = {
    "users": [
        {"hour": 11, "total": 100, "active": 75, "inactive": 25},
        {"hour": 12, "total": 150, "active": 100, "inactive": 50},
    ]
}
