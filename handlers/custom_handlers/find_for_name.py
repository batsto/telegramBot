
from telebot import types, custom_filters
from loader import bot
from api.get_movie import get_movie_by_name
from keyboards.inline.find_for_name import keyboard_genres
from utils.output_films import output_films_in_chat
from telebot.states.sync.context import StateContext
from states.custom.find_for_name import FindForName




@bot.message_handler(func=lambda m: m.text == "🔍 Поиск по названию")
def search_for_name(message: types.Message, state: StateContext) -> None:
    """Cпрашивает у пользователя название фильма"""

    state.set(FindForName.query)
    bot.send_message(chat_id=message.chat.id,
                           text="Введите название фильма, который хотите найти"
                            )



@bot.message_handler(state=FindForName.query)
def chose_genres(message: types.Message, state: StateContext) -> None:
    """Cпрашивает у пользователя жанр"""

    state.set(FindForName.genre)
    bot.send_message(chat_id=message.chat.id,
                           text="Выбирите жанр:",
                           reply_markup=keyboard_genres())
    state.add_data(query=message.text)



@bot.callback_query_handler(state=FindForName.genre)
def chose_quantity(call: types.CallbackQuery, state: StateContext) -> None:
    """Cпрашивает у пользователя количество выводимых результатов"""

    state.set(FindForName.quantity)
    genre = call.data
    if genre != "cancel":  # пропускает выбор жанра
        state.add_data(genre=genre)

    bot.send_message(chat_id=call.message.chat.id,
                            text="Сколько результатов поиска хотите увидеть? (1-10)",
                            reply_markup=None
                     )



@bot.message_handler(state=FindForName.quantity)
def process_quantity(message: types.Message, state: StateContext) -> None:
    """Выволит результаты пойска"""
    try:
        quantity= int(message.text)

        if quantity<1 or quantity>10:
            bot.send_message(message.chat.id, "Введите число от 1 до 10!")
            return



        search_query = state.data()
        films_info = get_movie_by_name(search_query)
        if films_info:
            output_films_in_chat(films_info, message, quantity)

        state.delete()


    except ValueError:
        bot.send_message(message.chat.id,
                         "Нужно ввести число")
    except Exception as e:
        print(f"Ошибка {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="Произошла ошибка при поиске. Попробуйте позже."
        )













