from telebot.types import Message, CallbackQuery
from loader import bot
from states.state_classes import BudgetMovie
from utils.output_films import print_message


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

    search_query = {"budget.value": budget, "page": page}

    # Печатаем в чат
    print_message(search_query, message=message)


@bot.callback_query_handler(state=BudgetMovie.budget)
def handle_pagination(call: CallbackQuery) -> None:
    '''Обрабаьывает нажатие кнопки следушие и предедущие '''
    # Получаем информацию
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        budget = data.get('budget')
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
    if call.data == "next":
        page_now = page + 1
    else:
        page_now = max(page - 1, 1)

    # Обновляем данные
    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data['page'] = page_now

    search_query = {"budget.value": budget, "page": page_now}

    # Отправляем данные в чат
    print_message(search_query, message=call.message)
