import os
import re
import ast
import time
import json
import schedule
from dotenv import load_dotenv
import undetected_chromedriver as uc
from utils_telegram import send_screenshot
from run_background import run_continuously
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from typing import Optional, Any, Tuple, List
from utils_navigation import init_scrollbar, scroll
from utils_processsing import process_elements, clear_game_list
from utils_telegram import telegram_sender, telegram_sender_photo, game_notification
from utils_db import save_wallet_statistic, create_tables_if_not_exists, collect_stat_bet


# Инициализация переменных
load_dotenv()
driver = None
action = None
game_list = []
scroll_step = 120
previous_scroll_position = 0
URL = 'https://www.fon.bet/live/football'

def load_cookies() -> None:
    """Загрузга данных входа"""
    global driver
    with open('cookies.json', 'r') as file:
        cookies = json.load(file)
        for cookie in cookies:
            driver.add_cookie(cookie)
    telegram_sender('Данные входа получены')
    # Перезагрузка страницы для применения cookies
    driver.refresh()

def boot_checker() -> None:
    """Проверяет готовность браузера и перезагружает при необходимости."""
    global driver, scrollbar
    count = 15
    while count > 0:
        try:
            init_scrollbar(driver)      # проверяем что скроллбар появился на странице
            time.sleep(1)
            return

        except:
            # Страница не загружена
            time.sleep(1)
            count -= 1

        if count == 0:
            driver.get("https://www.fon.bet/live/football")
            time.sleep(2)
            count = 15                  # Сброс счетчика попыток

def stop_scaner() -> None:
    global driver
    """Останавливает сканирование"""
    run_continuously().set()            # остановка цикла задач сканирования
    if driver is not None:
        driver.close()                  # закрытие окна
        driver.quit()                   # разрыв соединения с сессией селениум


def search_games() -> None:
    """Сканирует игры."""
    global game_list, driver, score_search, previous_scroll_position
    try:
        main_elements = driver.find_elements(By.CLASS_NAME, "sport-base-event-wrap--WmtIb")
        for element in main_elements:
            process_elements(element, driver)
        scroll(previous_scroll_position)
    except Exception as e:
        telegram_sender(f'<b>Ошибка цикла:<\b>\n{e}')
        send_screenshot(driver)          # при ошибке центрального отправка скриншота
        boot_checker()                   # проверка сайта, перзагрузка

def main() -> None:
    """Основная функция запуска"""
    global driver, action, game_list, scroll_step
    chrome_options = uc.ChromeOptions()

    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')
    chrome_options.add_argument('--disable-setuid-sandbox')
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--window-size=1920,1080")

    driver = uc.Chrome(use_subprocess=True, chrome_options=chrome_options)
    telegram_sender('Запуск браузера, открытие страницы')
    driver.get(URL)
    #load_cookies()                 # загрузка данных входа
    boot_checker()                  # проверка вебстраница загружена
    telegram_sender('Страница загружена, начало сканирования')

    if os.name != 'nt':             # Проверка, что операционная система не Windows
        try:
            create_tables_if_not_exists()
        except Exception as e:
            telegram_sender(f'База данных: \n{e}')

    action = ActionChains(driver)
    schedule.every(40).minutes.do(clear_game_list)
    schedule.every().second.do(search_games)
    run_continuously()

if __name__ == '__main__':
    main()