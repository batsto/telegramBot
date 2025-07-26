from telebot import types
from loader import bot
from keyboards.inline.find_for_name import keyboard_genres
from utils.output_films import  print_message
from states.state_classes import FindForName


@bot.message_handler(func=lambda m: m.text == "🔍 Поиск по названию")
def search_for_name(message: types.Message) -> None:
    """Cпрашивает у пользователя название фильма"""

    bot.set_state(user_id=message.from_user.id,
                  chat_id=message.chat.id,
                  state=FindForName.query)
    bot.send_message(chat_id=message.chat.id,
                     text="Введите название фильма, который хотите найти:")


@bot.message_handler(state=FindForName.query)
def chose_genres(message: types.Message) -> None:
    """Cпрашивает у пользователя жанр"""

    #Сохраняем промежуточную информацию
    with bot.retrieve_data(user_id=message.from_user.id, chat_id=message.chat.id) as data:
        data['query'] = message.text

    bot.set_state(user_id=message.from_user.id,
                  chat_id=message.chat.id,
                  state=FindForName.genre)
    bot.send_message(chat_id=message.chat.id,
                     text="Выбирите жанр:",
                     reply_markup=keyboard_genres())


@bot.callback_query_handler(state=FindForName.genre)
def chose_quantity(call: types.CallbackQuery) -> None:
    """Cпрашивает у пользователя количество выводимых результатов"""

    # Удаляем клавиатуру
    bot.delete_message(chat_id=call.message.chat.id,
                       message_id=call.message.message_id)
    genre = call.data
    genre_text = 'Выбор жанра отменен!' if genre == "cancel" else f'Жанр: {genre}'

    with bot.retrieve_data(user_id=call.from_user.id, chat_id=call.message.chat.id) as data:
        data['genre'] = genre
    bot.send_message(chat_id=call.message.chat.id,
                     text=f"{genre_text}\n"
                          f"Сколько результатов поиска хотите увидеть? (1-10)",
                     reply_markup=None)

    bot.set_state(user_id=call.from_user.id,
                  chat_id=call.message.chat.id,
                  state=FindForName.quantity)


@bot.message_handler(state=FindForName.quantity)
def process_quantity(message: types.Message) -> None:
    """Выволит результаты пойска"""
    try:
        quantity = int(message.text)
        if quantity < 1 or quantity > 10:
            bot.send_message(chat_id=message.chat.id,
                             text="Введите число от 1 до 10!")
            return

        with bot.retrieve_data(message.from_user.id, message.chat.id) as data:
            search_query = {
                'query': data.get('query'),
                'genre': data.get('genre')}

        print_message(data=search_query, message=message, quantity=quantity)

    except ValueError:
        bot.send_message(message.chat.id,
                         "Нужно ввести число")
    finally:
        bot.delete_state(user_id=message.from_user.id, chat_id=message.chat.id)
