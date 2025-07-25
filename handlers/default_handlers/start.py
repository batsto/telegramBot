from telebot.types import Message
from keyboards.reply.main_menu import main_menu_keyboards
from loader import bot


@bot.message_handler(commands=["start"])
def bot_start(message: Message):
    welcome_text = f"""
    <b>Привет, {message.from_user.full_name}</b>👋
    
    Этот телеграм-бот предназначен для поиска фильмов и сериалов по различным критериям.
    что бы продолжить нажми <b>меню</b> ↓ .
    """
    bot.send_message(
        message.chat.id,
        welcome_text,
        parse_mode="HTML",
        reply_markup=main_menu_keyboards(),
    )
