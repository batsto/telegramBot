from telebot import types


def get_main_menu_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button = types.KeyboardButton("Меню")
    keyboard.add(button)
    return keyboard
