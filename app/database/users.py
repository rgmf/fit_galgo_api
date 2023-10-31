from bson.objectid import ObjectId

from app.database.database import DbManager
from app.database.models.users import UserIn, UserDb
from app.config import Settings


class UserManager(DbManager):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)

    def drop(self) -> None:
        self._client.drop_collection("users")

    def get(self) -> list[UserDb]:
        users: list[dict] = self._client.users.find()
        return [UserDb.from_database_dict(user) for user in users]

    def get_by_username(self, username: str) -> UserDb | None:
        user: dict | None = self._client.users.find_one({"username": username})
        return UserDb.from_database_dict(user) if user else None

    def insert(self, user: UserIn) -> str:
        id: ObjectId = self._client.users.insert_one(user.model_dump()).inserted_id
        return str(id)
