from telebot import types
from loader import bot
from keyboards.reply.main_menu import main_menu_keyboards


@bot.message_handler(func=lambda m: m.text in ("Меню", "Фильмы не найдены. Попробуйте другой запрос."))
def main_menu(message: types.Message) -> None:
    bot.send_message(message.chat.id, f"Выбирайте", reply_markup=main_menu_keyboards())

