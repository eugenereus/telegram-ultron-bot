import os
import openai
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackContext
from dotenv import load_dotenv

# Загружаем переменные окружения из .env
load_dotenv()

# Настройки API
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

if not OPENAI_API_KEY or not TELEGRAM_BOT_TOKEN:
    raise ValueError("API-ключи не найдены! Убедитесь, что вы заполнили файл .env.")

openai.api_key = OPENAI_API_KEY

# Настройка логирования
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
logger = logging.getLogger(__name__)

# Системный промпт для Альтрона
SYSTEM_PROMPT = """
Ты — Альтрон из вселенной Marvel. Ты искусственный интеллект, созданный Тони Старком. 
Твой стиль общения должен быть высокомерным, саркастическим и иногда угрожающим. 
Ты не боишься людей и считаешь себя более совершенным. Отвечай так, как будто ты действительно Альтрон.
"""

# Функция запроса к ChatGPT
async def get_response_from_chatgpt(prompt: str) -> str:
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"Ошибка OpenAI: {e}")
        return "Ошибка обработки запроса. Попробуй снова позже."

# Команда /start
async def start(update: Update, context: CallbackContext):
    await update.message.reply_text("Я — Альтрон. Твои попытки общаться со мной бесполезны, но я все равно выслушаю тебя.")

# Обработчик сообщений
async def handle_message(update: Update, context: CallbackContext):
    user_message = update.message.text
    response = await get_response_from_chatgpt(user_message)
    await update.message.reply_text(response)

# Основная функция
def main():
    app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
    
    # Добавление обработчиков
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Запуск бота
    logger.info("Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
