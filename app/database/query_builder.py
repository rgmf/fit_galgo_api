from datetime import datetime


class QueryBuilder:
    def __init__(self):
        self._query_dict: dict[str, dict] = {}

    def eq(self, field: str, value: str):
        self._query_dict[field] = value

    def from_date(self, value: datetime, without_time: bool = False):
        final_value: any = value
        if without_time:
            final_value = value.date().strftime("%Y%m%d")

        if "dates_between" not in self._query_dict:
            self._query_dict["dates_between"] = {}
        self._query_dict["dates_between"]["$gte"] = final_value

    def to_date(self, value: datetime, without_time: bool = False):
        final_value: any = value
        if without_time:
            final_value = value.date().strftime("%Y%m%d")

        if "dates_between" not in self._query_dict:
            self._query_dict["dates_between"] = {}
        self._query_dict["dates_between"]["$lte"] = final_value

    def get_query(self) -> dict[str, dict]:
        return self._query_dict
