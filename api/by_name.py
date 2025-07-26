from typing import List
from config_data.config import  SEARCH_URL
from api.get_movie import get_movie



def get_movie_by_name(query: dict) -> List:
    return get_movie(query, SEARCH_URL)