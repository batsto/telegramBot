from typing import List
from api.by_name import get_movie_by_name
from api.by_rating import get_movie_by_rating
from loader import bot
from telebot import types
from .create_str_text import create_str
from keyboards.inline.movie_by_rating import next_button, next_previous_button


def output_films_in_chat(data: List, message: types.Message, quantity: int = 10) -> None:
    """Печатает фильмы в чат"""
    if not data:
        bot.send_message(message.chat.id, "Фильмы не найдены. Попробуйте другой запрос.")
        return

    bot.send_message(message.chat.id, "🔍 Результаты поиска:\n\n")
    for ind, film in enumerate(data):
        if ind < quantity:
            text_film = create_str(film)

            poster = film.get("poster", {}).get("url")
            if poster:
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=poster,
                    caption=text_film
                )


def print_message(data: dict, message: types.Message, quantity: int = 10):
    try:
        if 'query' in data:
            films_info = get_movie_by_name(data)
            if films_info:
                output_films_in_chat(films_info, message, quantity)

        else:
            films_info = get_movie_by_rating(data)
            page = data.get('page')
            if films_info:
                # Выводим сообщение в чат
                output_films_in_chat(films_info, message=message)

                # Определяем какую клавиатуру показывать
                reply_markup = next_button() if page == 1 else next_previous_button()

                # Отправляем клавиатуру
                bot.send_message(chat_id=message.chat.id,
                                 text="Выбирите действие",
                                 reply_markup=reply_markup)

    except Exception as e:
        print(f"Ошибка {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="Произошла ошибка при поиске. Попробуйте позже.")
        bot.delete_state(user_id=message.from_user.id,
                         chat_id=message.chat.id)