from typing import List
from utils.constants import SELECT_FIELDS, MOVIE_URL, SEARCH_URL
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


def get_movie_by_name(query: dict) -> List:
    return get_movie(query, SEARCH_URL)

def get_movie_by_rating(query: dict) -> List:
    return get_movie(query, MOVIE_URL)