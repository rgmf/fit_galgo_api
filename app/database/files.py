from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from fit_galgo.fit.models import FitModel
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from pymongo.cursor import Cursor
from fit_galgo.fit.models import FileId

from app.database.database import DbManager
from app.config import Settings
from app.database.models.users import User

COLLECTION_NAME = {
    "default": "generic",
    "activity": "activity",
    "monitoring_a": "monitoring",
    "monitoring_b": "monitoring",
    "monitoring": "monitoring",
    68: "hrv",
    "68": "hrv",
    49: "sleep",
    "49": "sleep"
}


class FilesManager(DbManager):
    def __init__(self, settings: Settings, user: User | None = None) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)
        self._user = user

    def insert(self, model: FitModel) -> str | None:
        """Inert a new model.

        :model FitModel: the model to be inserted.

        :return: the new document's id inserted into MongoDb or None if
                 document already exists (duplicated key).
        """
        model_dict: dict = model.model_dump()
        model_dict["_id"] = self.generate_id(model.file_id)
        model_dict["username"] = self._user.username if self._user else None
        jsonable_model = jsonable_encoder(model_dict)
        try:
            collection_name: str = self.get_collection_name(model.file_id)
            collection: Collection = self._client[collection_name]
            id: ObjectId = collection.insert_one(jsonable_model).inserted_id
        except DuplicateKeyError:
            return None
        return str(id)

    def generate_id(self, file_id: FileId) -> str:
        type_: str = str(file_id.file_type)
        date_created: str = (
            file_id.time_created.strftime("%Y%m%d%H%M%S") if file_id.time_created else ""
        )
        return f"{type_}_{date_created}"

    def get_collection_name(self, file_id: FileId) -> str:
        return (
            COLLECTION_NAME[file_id.file_type]
            if file_id.file_type in COLLECTION_NAME
            else COLLECTION_NAME["default"]
        )

    def drop(self, collection_name: str) -> None:
        self._client.drop_collection(collection_name)

    def get(self, collection_name: str) -> Cursor | None:
        collection = self._client[collection_name]
        if collection is not None:
            return collection.find()
        return None
