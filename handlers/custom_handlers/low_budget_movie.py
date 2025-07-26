from telebot.types import Message, CallbackQuery
from loader import bot
from api.get_movie import get_movie_by_rating
from states.state_classes import BudgetMovie
from utils.output_films import output_films_in_chat
from keyboards.inline.low_budget_movie import next_previous_button, next_button


def print_message(budget: str, page: int, message: Message):
    try:
        films_info = get_movie_by_rating({"budget.value": budget, "page": page})
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






@bot.message_handler(func=lambda m: m.text in ("💰 Недорогие фильмы", "💎 Дорогие фильмы"))
def get_movie(message: Message) -> None:
    """Спрашивает у пользователя бюджет"""
    # Устанавливаем состояние
    bot.set_state(user_id=message.from_user.id,
                  chat_id=message.chat.id,
                  state=BudgetMovie.budget)

    budget = "1000-6666666" if message.text == "💰 Недорогие фильмы" else "6666666-1000000000"
    page = 1

    # Сохраняем состояние
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        data['budget'] = budget
        data['page'] = page

    # Печатаем в чат
    print_message(budget=budget, page=page, message=message)





@bot.callback_query_handler(state=BudgetMovie.budget)
def handle_pagination(call: CallbackQuery) -> None:
    '''Обрабаьывает нажатие кнопки следушие и предедущие '''
    # Получаем информацию
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        budget = data.get('rating')
        page = data.get('page', 1)

    if not budget:
        bot.answer_callback_query(callback_query_id=call.message.chat.id,
                                  text=f"Ошибка. Попробуйте заново\n"
                                       f"Нажмите /start ")

        bot.delete_state(user_id=call.from_user.id,
                      chat_id=call.message.chat.id)
        return

    # Удаляем старое сообщение
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)

    # Определяем направление пагинации
    if call.data == "next_budget":
        page_now = page + 1
    else:
        page_now = max(page - 1, 1)

    # Обновляем данные
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data['page'] = page_now

    # Отправляем данные в чат
    print_message(budget=budget, page=page_now, message=call.message)


