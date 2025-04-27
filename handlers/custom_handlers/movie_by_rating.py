from telebot.types import Message, CallbackQuery
from loader import bot
from api.movie_by_rating import get_movie_by_rating
from utils.create_str_text import create_str
from utils.output_films import output_films_in_chat
from keyboards.inline.movie_by_rating import next_button, next_previous_button

user_info = {}


@bot.message_handler(func=lambda m: m.text == "⭐ Фильмы по рейтингу")
def input_rating(message: Message) -> None:
    """Спрашивает у пользователя рейтинг"""
    msg = bot.send_message(message.chat.id,
                     "Введите с каким рейтингом хотите увидеть фильмы. Пример: 10, 9, 5.2")
    bot.register_next_step_handler(msg, rating_movie)




def rating_movie(message: Message) -> None:
    """Проверяет рейтинг и выводит результаты поиска в чат"""
    try:
        rating = float(message.text.replace(",", "."))
        if  not 1 <= rating <= 10:
            bot.send_message(chat_id=message.chat.id,
                             text="Рейтинг должен быть от 0 до 10. Попробуйте снова.")
            return

        user_info[message.from_user.id] = {"rating.kp": rating, "page": 1}

        films_info = get_movie_by_rating(user_info[message.from_user.id])
        output_films_in_chat(films_info, message=message)

        bot.send_message(chat_id=message.chat.id,
                         text="Выбирите действие",
                         reply_markup=next_button())

    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text="Введите число")
    except Exception as e:
        print(f"Ошибка {e}")
        bot.send_message(
            chat_id=message.chat.id,
            text="Произошла ошибка при поиске. Попробуйте позже."
        )



@bot.callback_query_handler(func=lambda c: c.data == "cancel")
def repiet_input_rating(call: CallbackQuery) -> None:
    """Спрашивает у пользователя рейтинг"""
    msg = bot.send_message(call.message.chat.id,
                           "Введите с каким рейтингом хотите увидеть фильмы. Пример: 10, 9, 5.2")
    bot.register_next_step_handler(msg, rating_movie)




@bot.callback_query_handler(func=lambda c: c.data == "next_rating")
def next_rating(call: CallbackQuery) -> None:
    user_data = user_info.get(call.from_user.id)
    if not user_data:
        bot.answer_callback_query(callback_query_id=call.message.chat.id,
                                  text="Ошибка. Попробуйте заново")
        return

    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)

    user_data['page']  += 1
    user_info[call.from_user.id] = user_data

    films_info = get_movie_by_rating(user_data)
    output_films_in_chat(films_info, message=call.message)


    bot.send_message(chat_id=call.message.chat.id,
                     text="Выбирите действие",
                     reply_markup=next_previous_button())


@bot.callback_query_handler(func=lambda c: c.data == "previous_button")
def previous_rating(call: CallbackQuery) -> None:
    user_data = user_info.get(call.from_user.id)
    if not user_data:
        bot.answer_callback_query(text="Ошибка. Попробуйте заново")
        return

    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)

    user_data['page'] -= 1
    user_info[call.from_user.id] = user_data

    films_info = get_movie_by_rating(user_data)
    output_films_in_chat(films_info, message=call.message)

    bot.send_message(chat_id=call.message.chat.id,
                     text="Выбирите действие",
                     reply_markup=next_button() if user_data['page']  == 1 else next_previous_button())

























