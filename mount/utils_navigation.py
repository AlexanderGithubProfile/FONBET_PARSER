import re
import time
import undetected_chromedriver as uc
from utils_telegram import telegram_sender
from selenium.webdriver.common.by import By
from selenium.common.exceptions import MoveTargetOutOfBoundsException

scroll_step = 120

def init_scrollbar(driver: uc.Chrome) -> None:
    """Инициализирует скроллбар."""
    global scrollbar
    scrollbar = driver.find_element(By.CLASS_NAME, 'sport-area__grow--EYgak').find_element(By.CLASS_NAME, 'scrollbar__thumb-panel__thumb--yq3xU')

def check_scroll() -> float:
    """Проверяет позицию скроллбара."""
    global scrollbar
    pattern = r"margin-top:\s*([0-9.]+)px;"
    match = re.search(pattern, scrollbar.get_attribute('style'))
    return float(match.group(1))

def action_scroll() -> None:
    """Производит скроллинг страницы."""
    global scroll_step, scrollbar, action
    from main import action
    try:
        action.click_and_hold(scrollbar).move_by_offset(0, scroll_step).release().perform()
        time.sleep(0.5)
    except MoveTargetOutOfBoundsException:
        scroll_step *= -1
        action_scroll()
    except Exception as e:
        telegram_sender(f'{e}')
        pass

def scroll(previous_scroll_position: float) -> None:
    """Управляет скроллингом в зависимости от позиции."""
    global scroll_step
    current_scroll = check_scroll()                 # проверка где сейчас скрол
    if abs(previous_scroll_position - current_scroll) < scroll_step * 0.5 and current_scroll > 1: # при уменьшении шага развернуть направление скрола
        scroll_step *= -1                           # разворот движения
        action_scroll()                             # действие скрол

    else:
        previous_scroll_position = check_scroll()   # переназначаем текущее положение скрола
        action_scroll()                             # действие скрол
        current_scroll = check_scroll()

        if abs(previous_scroll_position - current_scroll) < scroll_step * 0.5 and current_scroll > 0 or current_scroll==0:
            scroll_step *= -1