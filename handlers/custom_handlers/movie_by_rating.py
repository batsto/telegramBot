from telebot.types import Message, CallbackQuery
from loader import bot
from api.get_movie import get_movie_by_rating
from utils.output_films import output_films_in_chat
from keyboards.inline.movie_by_rating import next_button, next_previous_button
from database.queries import save_search_request, get_user_search_request




@bot.message_handler(func=lambda m: m.text == "⭐ Фильмы по рейтингу")
def input_rating(message: Message) -> None:
    """Спрашивает у пользователя рейтинг"""
    msg = bot.send_message(chat_id=message.chat.id,
                           text="Введите с каким рейтингом хотите увидеть фильмы. Пример: 10, 9, 5.2")
    bot.register_next_step_handler(msg, rating_movie)



def rating_movie(message: Message) -> None:
    """Проверяет рейтинг и выводит результаты поиска в чат"""
    try:
        # Получаем рейтинг от пользователя
        rating_now = float(message.text.replace(",", "."))
        if  not 1 <= rating_now <= 10:
            msg = bot.send_message(chat_id=message.chat.id,
                             text="Рейтинг должен быть от 0 до 10. Попробуйте снова.")
            bot.register_next_step_handler(msg, input_rating)
        # Сохраняем данные в бд
        save_search_request(user_id=message.from_user.id,
                            rating=rating_now,
                            page=1)
        # Получаем данные для новой страницы
        films_info = get_movie_by_rating({"rating.kp": rating_now, "page": 1})
        if films_info:
            # Выводим сообщение в чат
            output_films_in_chat(films_info, message=message)

            # Отправляем клавиатуру
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
    """Спрашивает у пользователя рейтинг после нажатия кнопки назад"""
    msg = bot.send_message(chat_id=call.message.chat.id,
                           text="Введите с каким рейтингом хотите увидеть фильмы. Пример: 10, 9, 5.2")
    bot.register_next_step_handler(msg, rating_movie)




@bot.callback_query_handler(func=lambda c: c.data in ["next_rating", "previous_button"])
def handle_pagination(call: CallbackQuery) -> None:
    '''Обрабаьывает нажатие кнопки следушие '''
    # Получаем информацию из бд
    user_data = get_user_search_request(call.from_user.id)
    if not user_data:
        bot.answer_callback_query(callback_query_id=call.message.chat.id,
                                  text="Ошибка. Попробуйте заново")
        print("Не найдена запись в базе данных")
        return

    # Удаляем старое сообщение
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)

    # Определяем направление пагинации
    current_page = user_data.get('page', 1)
    if call.data=="next_rating":
        page_now = current_page + 1
    else:
        page_now = max(current_page - 1, 1)

    # Обновляем данные в бд
    rating_now = user_data.get('rating', 0)
    save_search_request(user_id=call.from_user.id,
                        rating=rating_now,
                        page=page_now)

    # Получаем фильмы для новой страницы
    films_info = get_movie_by_rating({"rating.kp": rating_now, "page": page_now})
    if films_info:
        # ОТправляем фильмы в чат
        output_films_in_chat(films_info, message=call.message)

        # Определяем какую клавиатуру показывать
        reply_markup = next_button() if page_now  == 1 else next_previous_button()

        # отпраляем клавиатуру
        bot.send_message(chat_id=call.message.chat.id,
                         text="Выбирите действие",
                         reply_markup=reply_markup)















