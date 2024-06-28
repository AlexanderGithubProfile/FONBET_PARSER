import os
import signal
import asyncio
import logging
from dotenv import load_dotenv
from utils_db import collect_stat_wallet
from run_background import run_continuously
from utils_telegram import send_screenshot
from utils_img import send_stat_to_telegram
from telegram import Update, Bot, __version__ as TG_VER
from main import main as starter, stop_scaner as stopper
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler

# Уровень логирования
logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.WARNING)
logger = logging.getLogger(__name__)

# Загрузка переменных окружения
load_dotenv()

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запуск основной функции."""
    starter()

async def stat(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запуск основной функции."""
    send_stat_to_telegram()

async def screen(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Запуск основной функции."""
    from main import driver
    send_screenshot(driver)

async def stop_func(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправка сообщения об остановке и завершение работы."""
    await context.bot.send_message(os.getenv('CHAT_ID'), "Бот остановлен")
    #collect_stat_wallet()                  # выполнить запись статистики текущего счета
    stopper()                               # завершить сессию
    #os.kill(os.getpid(), signal.SIGINT)

async def turned_on() -> None:
    """Отправка приветственного сообщения и стикера."""
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'))
    await bot.send_sticker(
        chat_id=os.getenv('CHAT_ID'),
        sticker='CAACAgIAAxkBAAIBwWY8iur1NohWGW1_lKvUC94E2PSwAAJuAAPb234AAUaeZ3EyOf6TNQQ'
    )
    keyboard = [
        [
            InlineKeyboardButton("Начать", callback_data="start"),
            InlineKeyboardButton("Остановка", callback_data="stop"),
        ],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await bot.send_message(
        chat_id=os.getenv('CHAT_ID'),
        text="<b>ЭТО FON_BOT</b>\nЯ помогу не пропустить",
        parse_mode='HTML', reply_markup=reply_markup
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка нажатий кнопок."""
    query = update.callback_query
    await query.answer()
    if query.data == "start":
        await start(query, context)
    if query.data == "stop":
        await stop_func(query, context)

def main() -> None:
    """Основная функция для запуска бота."""
    application = Application.builder().token(os.getenv('TELEGRAM_TOKEN')).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("stop", stop_func))
    application.add_handler(CommandHandler("stat", stat))
    application.add_handler(CommandHandler("screen", screen))
    application.add_handler(CallbackQueryHandler(button))
    loop = asyncio.get_event_loop()
    loop.run_until_complete(turned_on())
    application.run_polling()

if __name__ == "__main__":
    main()