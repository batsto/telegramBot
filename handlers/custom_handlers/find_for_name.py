from telebot import types
from loader import bot
from api.get_ten_movies import get_ten_films_list
import json



@bot.message_handler(func=lambda m: m.text == "🔍 Поиск по названию")
def main_menu(message: types.Message) -> None:
    msg = bot.send_message(message.chat.id, "Напишите название фильма, который хотите найти:")
    bot.register_next_step_handler(msg, search_for_name)



@bot.message_handler(func=lambda m: True)
def search_for_name(message: types.Message) -> None:
    global genres_str
    try:
        films_info = get_ten_films_list(message.text)

        if not films_info:
            bot.send_message(message.chat.id, "Фильмы не найдены. Попробуйте другой запрос.")
            return

        bot.send_message(message.chat.id, "🔍 Результаты поиска:\n\n")
        for film in films_info:

            genres = film.get("genres", [])
            if genres:
                genres_str = ", ".join([item.get('name', '') for item in genres])
            else:
                genres_str = "Не указаны"

            text_film = (
                f"Название: {film.get('name', 'Название не известно.')}\n"
                f"Описание: {film.get('description', 'Описания нет.')}\n"
                f"Год: {film.get('year', 'Год не указан.')}\n"
                f"Рейтинг: {film['rating'].get('kp', 'Рейтинг не указан')}\n"
                f"Жанр: {genres_str}\n"
                f"Возраст: {film.get('ageRating', 'Не указан')}"
            )

            if film["poster"]["url"]:
                bot.send_photo(
                    chat_id=message.chat.id,
                    photo=film["poster"]["url"],
                    caption=text_film
                )

    except Exception as e:
        print(f"Ошибка {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="Произошла ошибка при поиске. Попробуйте позже."
        )













