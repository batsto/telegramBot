
from telebot import types
from loader import bot
from api.get_movie import get_movie_by_name
from keyboards.inline.find_for_name import keyboard_genres
from utils.output_films import output_films_in_chat
from database.queries import save_search_request, get_user_search_request





@bot.message_handler(func=lambda m: m.text == "🔍 Поиск по названию")
def search_for_name(message: types.Message) -> None:
    """Cпрашивает у пользователя название фильма"""
    msg = bot.send_message(chat_id=message.chat.id,
                         text="Введите название фильма, который хотите найти",
                            )
    bot.register_next_step_handler(msg, chose_genres)



def chose_genres(message) -> None:
    """Cпрашивает у пользователя жанр"""
    #search_query["query"] = message.text
    save_search_request(user_id=message.from_user.id,
                        query=message.text)

    bot.send_message(chat_id=message.chat.id,
                           text="Выбирите жанр:",
                           reply_markup=keyboard_genres())


@bot.callback_query_handler(func=lambda call: call.data.startswith("genre_"))
def chose_quantity(call) -> None:
    """Cпрашивает у пользователя количество выводимых результатов"""

    genre_now = call.data.replace("genre_", "")
    if genre_now != "cancel":  # пропускает выбор жанра
        #search_query["genres.name"] = genre
        save_search_request(user_id=call.from_user.id,
                            genre=genre_now)

    msg = bot.send_message(chat_id=call.message.chat.id,
                            text="Сколько результатов поиска хотите увидеть? (1-10)",
                            reply_markup=None
                     )
    bot.register_next_step_handler(msg, process_quantity)



def process_quantity(message: types.Message) -> None:
    """Выволит результаты пойска"""
    try:
        quantity_now = int(message.text)

        if 1 <= quantity_now <= 10:
            #search_query["limit"] = quantity
            save_search_request(user_id=message.from_user.id,
                                quantity=quantity_now)
        else:
            bot.send_message(message.chat.id, "Введите число от 1 до 10!")
            return


        #films_info = get_movie_by_name(search_query)
        search_query = get_user_search_request(user_id=message.from_user.id)
        print(search_query)
        films_info = get_movie_by_name(search_query)
        if films_info:
            output_films_in_chat(films_info, message)


    except ValueError:
        bot.send_message(message.chat.id,
                         "Нужно ввести число")
    except Exception as e:
        print(f"Ошибка {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="Произошла ошибка при поиске. Попробуйте позже."
        )













