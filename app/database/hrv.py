from pymongo.cursor import Cursor

from app.database.database import DbManager
from app.database.models import Hrv, User
from app.config import Settings


class HrvManager(DbManager):
    def __init__(self, settings: Settings, user: User) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)
        self._user: User = user

    def get(self) -> list[Hrv]:
        filter: dict[str, any] = {
            "username": self._user.username
        }

        if self._query_builder and "dates_between" in self._query_builder.get_query():
            filter["summary.timestamp"] = (
                self._query_builder.get_query()["dates_between"]
            )

        hrv: Cursor = self._client.hrv.find(filter).sort("summary.timestamp")

        return [Hrv(**h) for h in hrv]
