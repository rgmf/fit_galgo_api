from pymongo.cursor import Cursor

from app.database.database import DbManager
from app.database.models import Monitor, User
from app.config import Settings


class MonitorManager(DbManager):
    def __init__(self, settings: Settings, user: User) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)
        self._user: User = user

    def get_monitor_with_steps(self) -> list[Monitor]:
        filter: dict[str, any] = {
            "username": self._user.username,
            "steps": {"$exists": True, "$ne": []}
        }

        if self._query_builder and "dates_between" in self._query_builder.get_query():
            filter["datetime_utc"] = self._query_builder.get_query()["dates_between"]

        monitor: Cursor = self._client.monitoring.find(filter).sort("datetime_utc", 1)

        return [Monitor(**m) for m in monitor]
