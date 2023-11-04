from pymongo.cursor import Cursor

from app.database.database import DbManager
from app.database.models import Activity, User
from app.config import Settings


class ActivitiesManager(DbManager):
    def __init__(self, settings: Settings, user: User) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)
        self._user = user

    def get(self) -> list[Activity]:
        filter: dict[str, any] = {"username": self._user.username}

        if self._query_builder and "dates_between" in self._query_builder.get_query():
            filter["session.timestamp"] = (
                self._query_builder.get_query()["dates_between"]
            )

        activities: Cursor = self._client.activity.find(filter).sort(
            "session.timestamp", 1
        )
        return [Activity(**activity) for activity in activities]
