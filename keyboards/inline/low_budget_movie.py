from telebot import types

def next_button():
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text="Следующие >", callback_data="next_budget")
    keyboard.add(button_1)

    return keyboard

def next_previous_button():
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text="Следующие >", callback_data="next_budget")
    button_2 = types.InlineKeyboardButton(text="< Предыдущие", callback_data="previous_budget")
    keyboard.add( button_2, button_1)
    return keyboard