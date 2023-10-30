from pymongo import MongoClient
from pymongo.cursor import Cursor
from fit_galgo.fit.models import FileId


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


class DbManager:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._client = self.get_db()

    def get_db(self):
        return MongoClient(host=self._host, port=self._port, tz_aware=True).fitgalgodb

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
