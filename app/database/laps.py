from pymongo.cursor import Cursor

from app.database.database import DbManager
from app.database.models import Lap, User
from app.config import Settings


class LapsManager(DbManager):
    def __init__(self, settings: Settings, user: User) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)
        self._user = user

    def get(self) -> list[Lap]:
        filter: dict[str, any] = {"username": self._user.username}

        if self._query_builder:
            for field, value in self._query_builder.get_query().items():
                filter[field] = value

        laps: Cursor = self._client.lap.find(filter).sort(
            "session.timestamp", 1
        )

        result: list[Lap] = []
        for lap in laps:
            result.append(Lap(**lap))

        return result
