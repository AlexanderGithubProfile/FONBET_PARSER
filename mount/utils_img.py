import os
import telebot
import pandas as pd
from PIL import Image
from io import BytesIO
from dotenv import load_dotenv
import matplotlib.pyplot as plt
from utils_telegram import telegram_sender_photo
from utils_db import get_latest_wallet_statistic

load_dotenv()
def send_stat_to_telegram() -> None:
    """Отправляет статистику кошелька в виде графика в Telegram."""
    latest_record = get_latest_wallet_statistic()
    df = pd.DataFrame(latest_record, columns=['Index', 'Date', 'Value']).sort_values(by='Index')
    df['Date'] = df['Date'].apply(lambda x: x.strftime('%d-%m-%y'))
    df['Moving Average'] = df['Value'].rolling(5).mean()

    # Создание графика
    plt.figure(figsize=(10, 6))
    bars = plt.bar(df['Index'], df['Value'], align='center', alpha=0.7)
    plt.plot(df['Index'], df['Moving Average'], color='red', marker='o', linestyle='-', linewidth=2, label='Скользящее среднее')

    for spine in plt.gca().spines.values(): # серая рамка графика
        spine.set_edgecolor('gray')

    plt.xlabel('ДАТА', fontsize=10, color='gray')
    plt.ylabel('ЗНАЧЕНИЕ', fontsize=10, color='gray')
    plt.xticks(color='gray')  # Поворот меток для лучшей читаемости
    plt.yticks(color='darkgray')
    plt.grid(True, color='lightgray', linestyle='--', linewidth=0.5, axis='y')
    plt.legend()
    plt.tight_layout()

    # Форматирование меток на столбцах
    for bar in bars:
        yval = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2., yval + 0.5, int(yval), ha='center', va='bottom', fontsize=10, color='gray')

    # Бинаризация графика и отправка в Telegram
    image_buffer = BytesIO()
    plt.savefig(image_buffer, format='png')
    plt.close()
    image_buffer.seek(0)
    telegram_sender_photo(image_buffer)

if __name__ == '__main__':
    send_stat_to_telegram()