from telebot.handler_backends import State, StatesGroup



class FindForName(StatesGroup):
    query = State()
    genre = State()
    quantity = State()