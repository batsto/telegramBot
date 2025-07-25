from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from typing import List

MOVIE_GENRES: List[List[str]] = [
    ["боевик", "boevik"],
    ["военный", "voennyy"],
    ["детектив", "detektiv"],
    ["драма", "drama"],
    ["комедия", "komediya"],
    ["криминал", "kriminal"],
    ["мелодрама", "melodrama"],
    ["мультфильм", "multfilm"],
    ["приключения", "priklyucheniya"],
    ["триллер", "triller"],
    ["ужасы", "uzhasy"],
    ["фантастика", "fantastika"],
    ["пропустить", "cancel"]
]


def keyboard_genres():
    keyboard = InlineKeyboardMarkup(row_width=3)
    buttons = [
        InlineKeyboardButton(text=name, callback_data=slug)
        for name, slug in MOVIE_GENRES
    ]

    keyboard.add(*buttons)
    return keyboard
