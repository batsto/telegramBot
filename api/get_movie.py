from typing import List
from config_data.config import SELECT_FIELDS
from .get_request import get_request_json






def get_movie(query: dict, url: str) -> List:
    response = get_request_json(url=url, params=query)
    if not response:
        return []

    docs = response.get("docs", [])

    filtered_docs = [
        {field: item[field] for field in SELECT_FIELDS if field in item}
        for item in docs
    ]

    return filtered_docs

