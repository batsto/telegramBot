from telebot.handler_backends import State, StatesGroup



class FindForName(StatesGroup):
    query = State()
    genre = State()
    quantity = State()

class MovieByRating(StatesGroup):
    rating = State()
    page = State()

class BudgetMovie(StatesGroup):
    budget = State()
    page = State()