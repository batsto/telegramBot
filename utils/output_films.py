from typing import List

from telebot import types
from loader import bot
from .create_str_text import create_str




def output_films_in_chat(data: List, message: types.Message) -> None:
        if not data:
            bot.send_message(message.chat.id, "Фильмы не найдены. Попробуйте другой запрос.")
            return

        bot.send_message(message.chat.id, "🔍 Результаты поиска:\n\n")
        for film in data:

            text_film = create_str(film)

            poster = film.get("poster", {}).get("url")
            if poster:
                    bot.send_photo(
                        chat_id=message.chat.id,
                        photo=poster,
                        caption=text_film
                    )



















