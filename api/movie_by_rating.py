from typing import List

from .get_request import get_request_json



SELECT_FIELDS = ["name", "description", "year", "rating", "genres", "ageRating", "poster"]


def get_movie_by_rating(query: dict) -> List:
    url = "https://api.kinopoisk.dev/v1.4/movie"

    response = get_request_json(url=url, params=query)
    docs = response.get("docs", [])

    filtered_docs = [
        {field: item[field] for field in SELECT_FIELDS if field in item}
        for item in docs
    ]

    return filtered_docs