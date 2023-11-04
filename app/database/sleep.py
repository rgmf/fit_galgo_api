from pymongo.cursor import Cursor

from app.database.database import DbManager
from app.database.models import Sleep, User
from app.config import Settings


class SleepManager(DbManager):
    def __init__(self, settings: Settings, user: User) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)
        self._user: User = user

    def get(self) -> list[Sleep]:
        filter: dict[str, any] = {
            "username": self._user.username
        }

        if self._query_builder and "dates_between" in self._query_builder.get_query():
            filter["dates"] = {
                "$elemMatch": self._query_builder.get_query()["dates_between"]
            }

        sleep: Cursor = self._client.sleep.find(filter)

        return [Sleep(**m) for m in sleep]
