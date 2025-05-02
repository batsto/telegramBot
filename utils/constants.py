from typing import List

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