
from api.get_request import get_request_json
from typing import List

SELECT_FIELDS = ["name", "description", "year", "rating", "genres", "ageRating", "poster"]


def get_ten_films_list(query: dict) -> List:
    url = "https://api.kinopoisk.dev/v1.4/movie/search"
    params = query

    response = get_request_json(url=url, params=params)
    docs = response.get("docs", [])

    filtered_docs = [
        {field: item[field] for field in SELECT_FIELDS if field in item}
        for item in docs
    ]

    return filtered_docs


