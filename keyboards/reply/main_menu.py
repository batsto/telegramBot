from telebot import types


def main_menu_keyboards():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    markup.add(types.KeyboardButton("🔍 Поиск по названию"))
    markup.add(types.KeyboardButton("⭐ Фильмы по рейтингу"))
    markup.add(types.KeyboardButton("💰 Недорогие фильмы"))
    markup.add(types.KeyboardButton("💎 Дорогие фильмы"))
    markup.add(types.KeyboardButton("📜 История поиска"))
    return markup
