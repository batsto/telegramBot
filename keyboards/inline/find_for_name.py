from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from typing import List

MOVIE_GENRES: List[List[str]] = [
    ["боевик", "genre_boevik"],
    ["военный", "genre_voennyy"],
    ["детектив", "genre_detektiv"],
    ["драма", "genre_drama"],
    ["комедия", "genre_komediya"],
    ["криминал", "genre_kriminal"],
    ["мелодрама", "genre_melodrama"],
    ["мультфильм", "genre_multfilm"],
    ["приключения", "genre_priklyucheniya"],
    ["триллер", "genre_triller"],
    ["ужасы", "genre_uzhasy"],
    ["фантастика", "genre_fantastika"],
    ["пропустить", "genre_cancel"]
]


def keyboard_genres():
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton(text=name, callback_data=slug)
        for name, slug in MOVIE_GENRES
    ]

    keyboard.add(*buttons)
    return keyboard
