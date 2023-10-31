from pymongo import MongoClient


class DbManager:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._client = self.get_db()

    def get_db(self):
        return MongoClient(host=self._host, port=self._port, tz_aware=True).fitgalgodb
