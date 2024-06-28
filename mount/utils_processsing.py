import re
import os
import time

import undetected_chromedriver as uc
from utils_db import collect_stat_bet
from typing import Tuple, Optional, Any
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from utils_telegram import telegram_sender, game_notification, send_screenshot

# Инициализация переменных
game_list = []          # фильтр лист команд
red_card = False        # флаг наличия красной карты
scroll_step = 120       # шаг прокрутки страницы парсером

def process_elements(element: Any, driver: uc.Chrome) -> None:
    """ Обработка элементов центральной таблицы игры на сайте
        Try-Exсept выполняют функцию отсечных фильтров для уменьшения цикла процесса"""
    try:
        name = element.find_element(By.CLASS_NAME, "sport-event__name--YAs00").text
        if ' — ' in name and name not in game_list:
            try:
                game_time = element.find_element(By.CLASS_NAME, "event-block-current-time__time--VEuoj")
                game_minutes = int(game_time.text.split(':')[0])        # количество пройденных минут игры
                if game_minutes >= int(os.getenv('GAME_MINUTES')):      # предварительный фильтр времени
                    try:
                        score = element.find_element(By.CLASS_NAME, "event-block-score__score--r0ZU9").text
                        hrefs = element.find_element(By.CSS_SELECTOR, "a[href*='/live/football/']").get_attribute('href')
                        bet1, bet2 = calc_bet(element, score)           # инициализация значений ставок с учетом варианта отсутствия одной из них
                        red_card = red_card_check(element, score)       # получена ли красная карта у проигрывающей команды

                        if bet1 is not None and bet2 is not None:
                            max_bet, min_bet = max(bet1, bet2), min(bet1, bet2)
                            if (min_bet <= float(os.getenv('MIN_BET')) and score in eval(os.getenv('SCORE'))) or max_bet >= float(os.getenv('MAX_BET')) or red_card:
                                game_notification(name, hrefs, game_time, score, bet1, bet2, driver, red_card)
                                game_list.append(name)                                      # фильтр игр для исключения дубликатов в сообщениях
                                # make_bet_for_game(element, driver, bet1, bet2, name)      # авто-расчет и выставление ставки
                    except:
                        pass
            except:
                pass
    except:
        pass

def red_card_check(element: Any, score: str) -> bool:
    """Получена ли красная карта у проигрывающей команды"""
    try:
        # Разделение счёта и поля красных карт на две int части
        score1, score2 = map(int, score.split(':'))
        card1, card2 = map(int, element.find_element(By.CSS_SELECTOR, '[style*="background-color: var(--localStatsRed_card);"]').text.split('-'))
        if (score1 < score2 and card1 > 0) or (score2 < score1 and card2) > 0:
            return True
    except:
        return False
def calc_cash_for_bet(driver: uc.Chrome, element: Any, bet1: Optional[float], bet2: Optional[float]) -> int:
    """Рассчитывает минимальную ставку."""
    try:
        min_bet_selector = 923 if bet1 > bet2 else 921  # селектор ставки с мин величиной
        bet_select_and_click = element.find_element(By.CSS_SELECTOR,
                                                    f'[data-testid="factorValue.{min_bet_selector}"]').click()
        time.sleep(1)
        cash_for_bet = int(float(driver.find_elements(By.CLASS_NAME, 'min-max--WkNVv')[0].text))
        telegram_sender(f'Мин ставка {cash_for_bet}')
        bet_detected=True                               # флаг присутствия поля ставки
    except:
        telegram_sender('Чтото с окном и мин.ставкой, ставка 50')
        cash_for_bet = 50                               # условная ставка
        bet_detected = False                            # флаг присутствия поля ставки
    collect_stat_bet(cash_for_bet, bet_detected)        # сохраняем статистику
    return cash_for_bet

def clear_selection_fill(driver: uc.Chrome, cash_for_bet: int) -> None:
    """Очистить поле и заполнить расчитанной ставкой"""
    try:
        field = driver.find_element(By.NAME, 'coupon-sum')
        while len(field.get_attribute('value')) > 0:
            field.send_keys(Keys.BACKSPACE)
        field.send_keys(str(cash_for_bet))
    except Exception as e:
        telegram_sender(f'Поле для ставки не заполнено. \nselected_name execption: {e}')

def make_bet_for_game(element: Any, driver: uc.Chrome, bet1: float, bet2: float, name: str) -> None:
    """Закрытие реклам, очистка поля ставки, заполнение, заключение ставки на игру."""
    try:
        clear_selector_and_close_commerial(driver, element)                 # снять предыдущий выбор, закрыть рекламу
        wallet_amount = float(driver.find_element(By.CLASS_NAME, '_relative--TTwjI').text) # сумма кошелька
        cash_for_bet = calc_cash_for_bet(driver, element, bet1, bet2)       # расчет ставки
        selected_name = extract_game_name(driver)                           # имя игры для проверки

        if wallet_amount > cash_for_bet:                                    # на счету меньше требуемого порога ввода
            clear_selection_fill(driver, cash_for_bet)                      # очистить поле ввода, ввести ставку
        else:
            telegram_sender(f'Треб. ставка больше общего кол-ва на счету')

        if name.split(" ")[0] == selected_name.split(" ")[0]:               # проверка - в поле ставки имя требуемой игры
            try:
                #bet_confirm = driver.find_element(By.CLASS_NAME, 'button-place--ctkF9').click()  # выставить ставку
                telegram_sender(f'Поля сверены, ставка выполнена')
            except:
                telegram_sender(f'Ошибка кнопки выставления ставки')
    except:
        pass

def calc_bet(element: Any, score: str) -> Tuple[Optional[float], Optional[float]]:
    """Инициализация значений ставок с учетом варианта отсутствия одной из них"""
    bet1, bet2 = None, None
    score1, score2 = map(int, score.split(':'))

    try:
        bet1 = float(element.find_element(By.CSS_SELECTOR, '[data-testid="factorValue.921"]').text)
    except:
        pass
    try:
        bet2 = float(element.find_element(By.CSS_SELECTOR, '[data-testid="factorValue.923"]').text)
    except:
        pass

    # Проверка - только одна ставка существует и она у ведущей команды
    if (bet1 is None and bet2 is not None) or (bet2 is None and bet1 is not None):
        if bet1 is None and score2 > score1:
            bet1 = 80
        elif bet2 is None and score1 > score2:
            bet2 = 80
    return bet1, bet2

def extract_game_name(driver: uc.Chrome) -> Optional[str]:
    # Поиск назв. игры в окне выставления ставки
    score_and_game = driver.find_element(By.CSS_SELECTOR, '[widget-class="widget.desktop.couponControl"]').text.split('\n')[4]
    line_ = re.search(r'(\d+:\d+)(.+)', score_and_game)
    if line_:
        score = line_.group(1)
        game_name = line_.group(2).strip()
        return game_name
    else:
        return None

def clear_game_list() -> None:
    """Очищает список игр."""
    global game_list
    game_list = []

def clear_selector_and_close_commerial(driver: uc.Chrome, element: Any) -> None:
    """Очищает селектор и закрывает рекламы"""
    # Закрыть окно селектора
    try:
        driver.find_element(By.CLASS_NAME, 'default-popup-container--eNZY7').find_element(By.CLASS_NAME,'svg--Nc79d').click()
    except:
        pass

    # Реклама
    try:
        driver.find_element(By.CLASS_NAME, 'svg--Nc79d').click()
    except:
        pass

    # Реклама
    try:
        driver.find_element(By.CLASS_NAME, 'coupon-cart-header--iWD5J').find_element(By.CLASS_NAME,'clear-outline--Cqh52').click()
    except:
        pass

