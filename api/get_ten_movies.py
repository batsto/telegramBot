
import requests
from config_data.config import KINOPOISK_API_KEY
from typing import List

SELECT_FIELDS = ["name", "description", "year", "rating", "genres", "ageRating", "poster"]


def get_ten_films_list(query: str) -> List:
    url = "https://api.kinopoisk.dev/v1.4/movie/search"
    headers = {"X-API-KEY": KINOPOISK_API_KEY}
    params = {"query": query, "limit": 10}

    response = requests.get(url, headers=headers, params=params).json()
    docs = response.get("docs", [])

    filtered_docs = [
        {field: item[field] for field in SELECT_FIELDS if field in item}
        for item in docs
    ]

    return filtered_docs


