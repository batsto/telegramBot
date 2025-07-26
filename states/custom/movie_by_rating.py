from telebot.handler_backends import State, StatesGroup



class MovieByRating(StatesGroup):
    rating = State()
    page = State()
