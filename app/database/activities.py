from typing import Annotated

from fastapi import Depends

from app.database.database import DbManager
from app.database.models import Activity, User
from app.database.query_builder import QueryBuilder
from app.auth.auth import get_auth_user
from app.config import Settings, get_settings


class ActivitiesManager(DbManager):
    def __init__(
            self,
            settings: Annotated[Settings, Depends(get_settings)],
            user: Annotated[User, Depends(get_auth_user)]
    ) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)
        self._user = user

    def get(self) -> list[Activity]:
        activities: list[dict] = self._client.activity.find(
            {"username": self._user.username}
        )
        return [Activity(**activity) for activity in activities]

    def filter(self, query: QueryBuilder) -> list[Activity]:
        activities: list[dict] = self._client.activity.find(
            {
                "$and": [
                    {"username": self._user.username},
                    query.get_query()
                ]
            }
        ).sort("session.timestamp", 1)
        return [Activity(**activity) for activity in activities]
