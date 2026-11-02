import os

import telebot
from dotenv import load_dotenv

from src.widget import mask_account_card

# Загружаем переменные из файла .env
load_dotenv()

# Безопасно достаем токен
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Ошибка: Токен бота не найден в файле .env!")

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
    """Приветственное сообщение при старте бота."""
    welcome_text = (
        "👋 Привет! Я бот для маскирования номеров карт и счетов.\n\n"
        "Отправьте мне строку в формате:\n"
        "👉 *Visa 1234567812345678*\n"
        "👉 *Счет 12345678901234567890*\n\n"
        "И я верну вам замаскированный результат!"
    )
    bot.reply_to(message, welcome_text, parse_mode="Markdown")


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    """Обработка любого текстового сообщения от пользователя."""
    user_input = message.text.strip()

    # Передаем текст в вашу функцию из ДЗ
    result = mask_account_card(user_input)

    # Используем срез [:7], чтобы проверить на ошибку
    if result[:7] == "Ошибка:":
        bot.reply_to(message, f"❌ {result}")
    else:
        bot.reply_to(message, f"✅ *Результат:* {result}", parse_mode="Markdown")


if __name__ == "__main__":
    print("Бот запущен и готов к работе...")
    bot.infinity_polling()