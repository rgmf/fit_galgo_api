from datetime import datetime


class QueryBuilder:
    def __init__(self):
        self._query_dict: dict[str, dict] = {}

    def from_date(self, value: datetime):
        if "dates_between" not in self._query_dict:
            self._query_dict["dates_between"] = {}
        self._query_dict["dates_between"]["$gte"] = value

    def to_date(self, value: datetime):
        if "dates_between" not in self._query_dict:
            self._query_dict["dates_between"] = {}
        self._query_dict["dates_between"]["$lte"] = value

    def get_query(self) -> dict[str, dict]:
        return self._query_dict
