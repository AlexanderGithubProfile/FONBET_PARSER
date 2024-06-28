import os
import telebot
from PIL import Image
from io import BytesIO
from typing import List
from dotenv import load_dotenv
import undetected_chromedriver as uc
from utils_db import get_latest_wallet_statistic

load_dotenv()

def telegram_sender_photo(image_buffer: BytesIO) -> None:
    """Отправляет изображение в Telegram."""
    bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
    bot.send_photo(os.getenv('CHAT_ID'), image_buffer)

def send_screenshot(driver) -> None:
    """Отправляет скриншот в Telegram."""
    if driver is None:
        telegram_sender('Сканирование еще не включено')
    else:
        img_byte = driver.get_screenshot_as_png()
        image_buffer = BytesIO(img_byte)
        telegram_sender_photo(image_buffer)

def telegram_sender(full_str: str) -> None:
    """Отправляет сообщение в Telegram."""
    try:
        bot = telebot.TeleBot(os.getenv('TELEGRAM_TOKEN'))
        bot.send_message(os.getenv('CHAT_ID'), full_str, parse_mode='HTML')
    except Exception as e:
        print(f'Ошибка отправщика телеграм {full_str}:\n{e}')
        pass
def game_notification(name: str, hrefs: List[str], game_time: str, score: str, bet1: float, bet2: float, driver: uc.Chrome, red_card: bool) -> None:
    """Шаблон сообщения"""
    message_str = (f'✉️<b>{name}\n| время:</b> <a href="{hrefs}">{game_time.text}</a> '
                   f'<b>| счет:</b> <a href="{hrefs}">{score}</a> '
                   f'<b>| коэф:</b> <a href="{hrefs}">{bet1} - {bet2}</a>|\n\n')
    if red_card:
        message_str += '• 🟥 - удаление у проигрывающей команды'
    if bet1 == 80 or bet2 == 80:
        message_str += '• ⬜️ - открыты ставки только на выигрывающую команду'
    telegram_sender(message_str)

