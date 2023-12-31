from bson.objectid import ObjectId
from fit_galgo.fit.models import FitModel
from pymongo.collection import Collection
from pymongo.errors import DuplicateKeyError
from pymongo.cursor import Cursor
from fit_galgo.fit.models import FileId, DistanceActivity, MultisportActivity
from pydantic import BaseModel

from app.database.database import DbManager
from app.config import Settings
from app.database.models import User

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
    def __init__(self, settings: Settings, user: User) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)
        self._user = user

    def drop(self, collection_name: str) -> None:
        self._client.drop_collection(collection_name)

    def insert(self, model: FitModel) -> str | None:
        """Inert a new model.

        :model FitModel: the model to be inserted.

        :return: the new document's id inserted into MongoDb or None if
                 document already exists (duplicated key).
        """
        def is_an_activity_with_records_and_laps(model: FitModel) -> bool:
            return (
                collection_name == COLLECTION_NAME["activity"] and
                (isinstance(model, DistanceActivity) or isinstance(model, MultisportActivity))
            )

        try:
            model_dict: dict = self._prepare_model_dict(model)
            collection_name: str = self.get_collection_name(model.file_id)
            collection: Collection = self._client[collection_name]

            inserted_id: ObjectId = collection.insert_one(model_dict).inserted_id
            if is_an_activity_with_records_and_laps(model):
                self._insert_records_and_laps(model, inserted_id)
        except DuplicateKeyError:
            return None

        return str(inserted_id)

    def _prepare_model_dict(self, model: FitModel) -> dict:
        model_dict = model.model_dump()
        model_dict["username"] = self._user.username
        model_dict["_id"] = self.generate_id(model.file_id, self._user.username)

        if isinstance(model, DistanceActivity) or isinstance(model, MultisportActivity):
            del model_dict["records"]
            del model_dict["laps"]

        return model_dict

    def _insert_records_and_laps(
            self, model: DistanceActivity | MultisportActivity, activity_id: ObjectId
    ) -> None:
        records_to_insert: list[dict] = self._prepare_models_to_insert(
            model.records, activity_id
        )
        if records_to_insert:
            self._client.record.insert_many(records_to_insert)

        laps_to_insert: list[dict] = self._prepare_models_to_insert(
            model.laps, activity_id
        )
        if laps_to_insert:
            self._client.lap.insert_many(laps_to_insert)

    def _prepare_models_to_insert(
            self, models: list[BaseModel], activity_id: ObjectId
    ) -> list[dict]:
        models_to_insert: list[dict] = []
        for model in models:
            model_dict = model.model_dump()
            model_dict["username"] = self._user.username
            model_dict["activity_id"] = activity_id
            models_to_insert.append(model_dict)
        return models_to_insert

    def generate_id(self, file_id: FileId, username: str) -> str:
        type_: str = str(file_id.file_type)
        date_created: str = (
            file_id.time_created.strftime("%Y%m%d%H%M%S") if file_id.time_created else ""
        )
        return f"{username}_{type_}_{date_created}"

    def get_collection_name(self, file_id: FileId) -> str:
        return (
            COLLECTION_NAME[file_id.file_type]
            if file_id.file_type in COLLECTION_NAME
            else COLLECTION_NAME["default"]
        )

    def get(self, collection_name: str) -> Cursor | None:
        collection = self._client[collection_name]
        if collection is not None:
            return collection.find()
        return None
