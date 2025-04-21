import requests
from typing import Any
from config_data.config import KINOPOISK_API_KEY

from requests import RequestException


def get_request_json(url: str, params: dict) -> Any:
    try:
        headers = {"X-API-KEY": KINOPOISK_API_KEY}
        response = requests.get(url=url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except RequestException as e:
        print(f"Api запрос не выполнен: {e}")
        return None
