from telebot import types

def next_button():
    keyboard = types.InlineKeyboardMarkup()  # Создаем новую клавиатуру каждый раз
    button_1 = types.InlineKeyboardButton(text="Следующие >", callback_data="next_rating")
    button_2 = types.InlineKeyboardButton(text="Назад", callback_data="cancel")
    keyboard.row(button_1)
    keyboard.row(button_2)
    return keyboard

def next_previous_button():
    keyboard = types.InlineKeyboardMarkup()  # Создаем новую клавиатуру каждый раз
    button_1 = types.InlineKeyboardButton(text="Следующие >", callback_data="next_rating")
    button_2 = types.InlineKeyboardButton(text="Назад", callback_data="cancel")
    button_3 = types.InlineKeyboardButton(text="< Предыдущие", callback_data="previous_button")
    keyboard.row( button_3, button_1)
    keyboard.row(button_2)
    return keyboard