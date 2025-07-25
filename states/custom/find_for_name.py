from telebot.states import State, StatesGroup



class FindForName(StatesGroup):
    query = State()
    genre = State()
    quantity = State()