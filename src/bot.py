import os
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer
import telebot
from dotenv import load_dotenv
from src.widget import mask_account_card

load_dotenv()
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not TOKEN:
    raise ValueError("Ошибка: Токен бота не найден в файле .env!")

bot = telebot.TeleBot(TOKEN)


# --- МИНИ-СЕРВЕР ДЛЯ БЕСПЛАТНОГО ХОСТИНГА ---
def run_health_server():
    class HealthCheckHandler(BaseHTTPRequestHandler):
        def do_GET(self):
            self.send_response(200)
            self.send_header("Content-type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Bot is alive!")

        def log_message(self, format, *args):
            return  # Отключаем лишние логи в консоли

    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), HealthCheckHandler)
    server.serve_forever()


# --------------------------------------------

@bot.message_handler(commands=["start", "help"])
def send_welcome(message):
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
    user_input = message.text.strip()
    result = mask_account_card(user_input)

    if result[:7] == "Ошибка:":
        bot.reply_to(message, f"❌ {result}")
    else:
        bot.reply_to(message, f"✅ *Результат:* {result}", parse_mode="Markdown")


if __name__ == "__main__":
    # Запускаем веб-заглушку в отдельном потоке, чтобы хостинг не ругался
    threading.Thread(target=run_health_server, daemon=True).start()

    print("Бот успешно запущен в режиме Production и готов к работе...")
    bot.infinity_polling()
