from telebot import types

def next_button():
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text="Следующие >", callback_data="next_budget")
    button_2 = types.InlineKeyboardButton(text="Назад", callback_data="cancel_budget")
    keyboard.row(button_1)
    keyboard.row(button_2)

    return keyboard

def next_previous_button():
    keyboard = types.InlineKeyboardMarkup()
    button_1 = types.InlineKeyboardButton(text="Следующие >", callback_data="next_budget")
    button_2 = types.InlineKeyboardButton(text="< Предыдущие", callback_data="previous_budget")
    button_3 = types.InlineKeyboardButton(text="Назад", callback_data="cancel_budget")
    keyboard.row( button_2, button_1)
    keyboard.row(button_3)

    return keyboard