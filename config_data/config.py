import os
from typing import List

from dotenv import load_dotenv, find_dotenv

if not find_dotenv():
    exit("Переменные окружения не загружены т.к отсутствует файл .env")
else:
    load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
KINOPOISK_API_KEY = os.getenv("KINOPOISK_API_KEY")

# Базовый URL API Кинопоиска
BASE_API_URL = "https://api.kinopoisk.dev/v1.4"

# URL для разных эндпоинтов
MOVIE_URL = f"{BASE_API_URL}/movie"
SEARCH_URL = f"{BASE_API_URL}/movie/search"

# Поля которые будем получать для фильмов
SELECT_FIELDS: List[str] = [
    "name",            # Название
    "description",     # Описание
    "year",            # Год выпуска
    "rating",          # Рейтинг
    "genres",          # Жанры
    "ageRating",       # Возрастной рейтинг
    "poster",          # Постер
    "id",              # ID фильма (часто полезно иметь)
    "movieLength",     # Длительность
]


DEFAULT_COMMANDS = (
    ("start", "Запустить бота"),
    ("help", "Вывести справку"),
)
