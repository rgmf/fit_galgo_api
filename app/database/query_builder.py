class QueryBuilder:
    def __init__(self):
        self._query_dict: dict[str, dict] = {}

    def gte(self, field: str, value: str) -> "QueryBuilder":
        if field in self._query_dict:
            query = self._query_dict[field]
        else:
            query: dict[str, str] = {}

        query["$gte"] = value

        self._query_dict[field] = query

        return self

    def lte(self, field: str, value: str) -> "QueryBuilder":
        query: dict[str, str] = self._query_dict[field] if field in self._query_dict else {}
        query["$lte"] = value
        self._query_dict[field] = query
        return self

    def get_query(self) -> dict[str, dict]:
        return self._query_dict
