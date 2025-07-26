from typing import List
from config_data.config import  MOVIE_URL
from api.get_movie import get_movie

def get_movie_by_rating(query: dict) -> List:
    return get_movie(query, MOVIE_URL)