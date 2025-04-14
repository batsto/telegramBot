from telebot.types import Message

from loader import bot


@bot.message_handler(commands=["help"])
def bot_help(message: Message):
    text = f"""
        <b>Привет, {message.from_user.full_name}</b>👋

        <b>🎬 Доступные команды:</b>

        <code>/movie_search</code> - поиск по названию
        <code>/movie_by_rating</code> - поиск по рейтингу
        <code>/low_budget_movie</code> - фильмы с низким бюджетом
        <code>/high_budget_movie</code> - фильмы с высоким бюджетом
        <code>/history</code> - история запросов
        """
    bot.send_message(message.chat.id, text, parse_mode="HTML")
