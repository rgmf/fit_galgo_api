from fastapi.encoders import jsonable_encoder
from bson.objectid import ObjectId
from fit_galgo.fit.models import FitModel
from pymongo.errors import DuplicateKeyError

from app.database.database import DbManager
from app.config import Settings


class FilesManager(DbManager):
    def __init__(self, settings: Settings) -> None:
        super().__init__(settings.mongodb_host, settings.mongodb_port)

    def insert(self, model: FitModel) -> str | None:
        """Inert a new model.

        :model FitModel: the model to be inserted.

        :return: the new document's id inserted into MongoDb or None if
                 document already exists (duplicated key).
        """
        model_dict: dict = model.model_dump()
        model_dict["_id"] = self.generate_id(model.file_id)
        jsonable_model = jsonable_encoder(model_dict)
        try:
            id: ObjectId = self._client.files.insert_one(jsonable_model).inserted_id
        except DuplicateKeyError:
            return None
        return str(id)

    def drop(self) -> None:
        self._client.drop_collection("files")
