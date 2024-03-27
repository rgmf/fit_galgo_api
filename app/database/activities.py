from pymongo.cursor import Cursor

from app.database.database import DbManager
from app.database.models import Activity, SetsActivity, SplitsActivity, MultiActivity, User
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

        result: list[Activity | MultiActivity | SetsActivity | SplitsActivity] = []
        for activity in activities:
            if "_id" in activity:
                activity["id"] = activity["_id"]
                del activity["_id"]

            if "sessions" in activity:
                result.append(MultiActivity(**activity))
            elif "sets" in activity and "session" in activity:
                result.append(SetsActivity(**activity))
            elif "splits" in activity and "session" in activity:
                result.append(SplitsActivity(**activity))
            else:
                result.append(Activity(**activity))

        return result
