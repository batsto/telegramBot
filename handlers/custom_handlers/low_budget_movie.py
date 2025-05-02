from telebot.types import Message, CallbackQuery
from loader import bot
from api.get_movie import get_movie_by_rating
from utils.output_films import output_films_in_chat
from keyboards.inline.low_budget_movie import next_previous_button, next_button





user_info = {}



@bot.message_handler(func=lambda m: m.text in ("💰 Недорогие фильмы", "💎 Дорогие фильмы"))
def get_movie(message: Message) -> None:

    budget = "1000-6666666" if message.text == "💰 Недорогие фильмы" else "6666666-1000000000"

    user_data = {"budget.value": budget, "page": 1}
    user_info[message.from_user.id] = user_data

    films_info = get_movie_by_rating(user_data)

    if films_info:
        output_films_in_chat(films_info, message)

        bot.send_message(chat_id=message.chat.id,
                         text="Выбирите действие",
                         reply_markup=next_button())




@bot.callback_query_handler(func=lambda c: c.data == "next_budget")
def get_next_budget(call: CallbackQuery) -> None:
    '''Обрабатывает нажатие кнопки следушие '''
    user_data = user_info[call.from_user.id]
    if not user_data:
        bot.send_message(chat_id=call.message.chat.id,
                         text="Ошибка. Попробуйте заново")

    user_data['page'] += 1
    films_info = get_movie_by_rating(user_data)
    if films_info:
        output_films_in_chat(films_info, call.message)

        bot.send_message(chat_id=call.message.chat.id,
                         text="Выбирите действие",
                         reply_markup=next_previous_button())





@bot.callback_query_handler(func=lambda c: c.data == "next_budget")
def get_previous_budget(call: CallbackQuery) -> None:
    '''Обрабатывает нажатие кнопки предыдущие'''
    user_data = user_info[call.from_user.id]
    if not user_data:
        bot.send_message(chat_id=call.message.chat.id,
                         text="Ошибка. Попробуйте заново")

    user_data['page'] -= 1
    films_info = get_movie_by_rating(user_data)
    if films_info:
        output_films_in_chat(films_info, call.message)

        bot.send_message(chat_id=call.message.chat.id,
                         text="Выбирите действие",
                         reply_markup=next_button() if user_data['page'] == 1 else next_previous_button())





