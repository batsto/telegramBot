from telebot.types import Message, CallbackQuery

from keyboards.reply.main_menu import main_menu_keyboards
from loader import bot
from api.get_movie import get_movie_by_rating
from states.state_classes import MovieByRating
from utils.output_films import output_films_in_chat
from keyboards.inline.movie_by_rating import next_button, next_previous_button



def print_message(rating: float, page: int, message: Message):
    try:
        films_info = get_movie_by_rating({"rating.kp": rating, "page": page})
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


@bot.message_handler(func=lambda m: m.text == "⭐ Фильмы по рейтингу")
def input_rating(message: Message) -> None:
    """Спрашивает у пользователя рейтинг"""
    bot.set_state(user_id=message.from_user.id,
                  chat_id=message.chat.id,
                  state=MovieByRating.rating)
    bot.send_message(chat_id=message.chat.id,
                     text="Введите с каким рейтингом хотите увидеть фильмы. Пример: 10, 9, 5.2")


@bot.message_handler(state=MovieByRating.rating)
def rating_movie(message: Message) -> None:
    """Проверяет рейтинг и выводит результаты поиска в чат"""
    try:
        # Получаем рейтинг от пользователя
        rating_now = float(message.text.replace(",", "."))
        page_now = 1
        if not 1 <= rating_now <= 10:
            bot.send_message(chat_id=message.chat.id,
                             text="Рейтинг должен быть от 0 до 10. Пожалуйста, попробуйте снова.\n"
                                  "Введите с каким рейтингом хотите увидеть фильмы:")
            return

        # Сохраняем данные
        with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
            data['rating'] = rating_now
            data['page'] = page_now

        # Отправляем данные в чат
        print_message(rating=rating_now, page=page_now, message=message)

        # Меняем состояние
        bot.set_state(user_id=message.from_user.id,
                      chat_id=message.chat.id,
                      state=MovieByRating.page)

    except ValueError:
        bot.send_message(chat_id=message.chat.id,
                         text="Рейтинг должен быть числом. Попробуйте снова.\n"
                              "Введите с каким рейтингом хотите увидеть фильмы:")




@bot.callback_query_handler(state='*', func=lambda c: c.data == "cancel")
def repiet_input_rating(call: CallbackQuery) -> None:
    """Логика после нажатия кнопки назад"""
    bot.delete_state(user_id=call.from_user.id,
                     chat_id=call.message.chat.id)
    bot.send_message(
        chat_id=call.message.chat.id,
        reply_markup=main_menu_keyboards())




@bot.callback_query_handler(state=MovieByRating.page)
def handle_pagination(call: CallbackQuery) -> None:
    '''Обрабаьывает нажатие кнопки следушие и предедущие '''
    # Получаем информацию
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        rating = data.get('rating')
        page = data.get('page', 1)

    if not rating:
        bot.answer_callback_query(callback_query_id=call.message.chat.id,
                                  text=f"Ошибка. Попробуйте заново"
                                       f"Введите с каким рейтингом хотите увидеть фильмы. Пример: 10, 9, 5.2")

        bot.set_state(user_id=call.from_user.id,
                      chat_id=call.message.chat.id,
                      state=MovieByRating.rating)
        return

    # Удаляем старое сообщение
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)

    # Определяем направление пагинации
    if call.data == "next_rating":
        page_now = page + 1
    else:
        page_now = max(page - 1, 1)

    # Обновляем данные
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data['page'] = page_now

    # Отправляем данные в чат
    print_message(rating=rating, page=page_now, message=call.message)

