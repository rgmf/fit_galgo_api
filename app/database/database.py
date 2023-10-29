from pymongo import MongoClient
from fit_galgo.fit.models import FileId


class DbManager:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._client = self.get_db()

    def get_db(self):
        return MongoClient(host=self._host, port=self._port, tz_aware=True).local

    def generate_id(self, file_id: FileId) -> str:
        type_: str = str(file_id.file_type)
        date_created: str = (
            file_id.time_created.strftime("%Y%m%d%H%M%S") if file_id.time_created else ""
        )
        return f"{type_}_{date_created}"
