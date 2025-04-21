

from telebot import types
from loader import bot
from api.get_ten_movies import get_ten_films_list
from utils.create_str_text import create_str
from keyboards.inline.find_for_name import keyboard_genres


search_query = {}



@bot.message_handler(func=lambda m: m.text == "🔍 Поиск по названию")
def search_for_name(message: types.Message) -> None:
    msg = bot.send_message(chat_id=message.chat.id,
                         text="Введите название фильма, который хотите найти",
                            )
    bot.register_next_step_handler(msg, chose_genres)



def chose_genres(message) -> None:
    search_query["query"] = message.text
    bot.send_message(chat_id=message.chat.id,
                           text="Выбирите жанр:",
                           reply_markup=keyboard_genres())


@bot.callback_query_handler(func=lambda call: call.data.startswith("genre_"))
def chose_quantity(call) -> None:
    bot.edit_message_reply_markup(
        chat_id=call.message.chat.id,
        message_id=call.message.text,
        reply_markup=None
    )
    search_query["genres.name"] = call.data.replace("genre_", "")
    msg = bot.send_message(chat_id=call.message.chat.id,
                     text="Сколько результатов поиска хотите увидеть? (1-10)"
                     )
    bot.register_next_step_handler(msg, process_quantity)



def process_quantity(message: types.Message) -> None:
    try:
        quantity = int(message.text)

        if 1 <= quantity <= 10:
            search_query["limit"] = quantity
        else:
            bot.send_message(message.chat.id, "Введите число от 1 до 10!")
            return


        films_info = get_ten_films_list(search_query)

        if not films_info:
            bot.send_message(message.chat.id, "Фильмы не найдены. Попробуйте другой запрос.")
            return

        bot.send_message(message.chat.id, "🔍 Результаты поиска:\n\n")
        for film in films_info:

            text_film = create_str(film)

            poster = film.get("poster", {}).get("url")
            if poster:
                    bot.send_photo(
                        chat_id=message.chat.id,
                        photo=poster,
                        caption=text_film
                    )

    except ValueError:
        bot.send_message(message.chat.id,
                         "Нужно ввести число")
    except Exception as e:
        print(f"Ошибка {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="Произошла ошибка при поиске. Попробуйте позже."
        )













