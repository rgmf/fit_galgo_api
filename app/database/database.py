from pymongo import MongoClient

from app.database.query_builder import QueryBuilder


class DbManager:

    def __init__(self, host, port):
        self._host = host
        self._port = port
        self._client = MongoClient(
            host=self._host, port=self._port, tz_aware=True
        ).fitgalgodb

        self._query_builder: QueryBuilder | None = None

    def add_query_builder(self, qb: QueryBuilder) -> None:
        self._query_builder = qb
