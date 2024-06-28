# FON BET SCANNER: Advanced Betting Alert System
- Удобный парсер для отслеживания событий на динамическом сайте, с обходом обнаружения автоматизации, работает без открытия окна и с уведомлениями в Telegram.

[English](./README_en.md) | [Русский](./README.md)

<p align="left">
 <img src="img/01_fon_bet_scanner_1.png" width="400">
 <img src="img/01_fon_bet_scanner_2.png" width="400">
</p>

## Использование 
Приложение в контейнере c работой без открытия окна, с включением исполняемым файлом для удобной работы без IDE (pycharm) и авто-запуском Docker
> - автоматизация управления - управление запуском и остановкой из чата, подгрузка данных входа через куки
> - скрипт имитирует поведение пользователя - скроллит страницу и собирает необходимые данные
> - режим полной автоматизации - расчет ставок и их выставление на основе собранных данных
> - отправка скриншотов в Telegram - текущий экран и визуализация статистики по счету отправляются в чат по команде
> - блокировка рекламы - скрипт автоматически закрывает всплывающие окна и рекламу

## Применяемые технологии
Скрипт выполнен с использованием следующих технологий и библиотек:
> - **[xvfb](https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml)**: виртуальный X-сервер для headless-браузера
> - **[fluxbox](https://fluxbox.org/)**: оконный менеджер для управления виртуальными окнами.
> - **[x11vnc](https://www.karlrunge.com/x11vnc/)**: VNC-сервер для удаленного управления виртуальными окнами.
> - **[openCV](https://opencv.org/)**: библиотека для обработки изображений
> - **[selenium + uc](https://www.selenium.dev/)**: средство для автоматизации веб-браузеров.
> - **[postgreSQL](https://www.postgresql.org)**: система управления базами данных.
> - **[requests](https://docs.python-requests.org/en/latest/)**: библиотека для HTTP-запросов.
> - **[docker](https://www.docker.com/)**: платформа контейнеризации приложений
> - **[telebot](https://pypi.org/project/pyTelegramBotAPI/)**: библиотека для работы с API Telegram.
> - **[pandas](https://pandas.pydata.org/)**: библиотека для работы с данными.
> - **[time](https://docs.python.org/3/library/time.html)**: библиотека для работы с временем.
> - **[schedule](https://schedule.readthedocs.io/en/stable/)**: библиотека для планирования задач.

<p align="left">
   <img src="img/02_fon_bet_scanner_1.png" width="400">
   <img src="img/02_fon_bet_scanner_2.png" width="400">
</p>

## Организация проекта

1. **fon_bet_scanner**: основной каталог проекта и настройки приложения.

    - `Dockerfile`: настройки Docker
    - `README.md`: файл с описанием проекта
    - `docker-compose.yml`: конфигурация для запуска
    - `docker_activate.bat`: сценарий активации Docker в Windows
    - `entrypoint.sh`: сценарий для запуска контейнера
    - `mount`: директория с основными скриптами
        - `bot_telegram.py`: скрипт для взаимодействия с Telegram.
        - `cookies.json`: файл с куками для входа.
        - `main.py`: основной файл запуска скрипта.
        - `run_background.py`: скрипт для фонового выполнения задач
        - `utils_db.py`: функции работы с базой данных
        - `utils_img.py`: функции для работы с изображениями
        - `utils_navigation.py`: функции навигации по сайту
        - `utils_processsing.py`: функции обработки элементов сайта
        - `utils_telegram.py`: функции работы с Telegram
    - `requirements.txt`: список зависимостей проекта.
      
- #### Создайте файл [.env](https://www.google.com/search?client=opera-gx&q=.env&sourceid=opera&ie=UTF-8&oe=UTF-8) в папке mount для настройки переменных окружения:
```dotenv 
# Образец требуемого файла .env
TELEGRAM_TOKEN=        # telegram_bot_token
CHAT_ID=               # telegram_chat_id
MIN_BET=               # минимальный_коэфициент_ставки
GAME_MINUTES=          # время_игры
MAX_BET=               # максимальный_коэфициент_ставки
SCORE=                 # счет_list_type
```
- #### Добавьте файл [cookies.json](https://en.wikipedia.org/wiki/HTTP_cookie) в папку mount:
```dotenv
# Выполните ручной вход на сайт и выполните скрипт
import time
import json
cookies = driver.get_cookies()
with open('cookies.json', 'w') as file:
    json.dump(cookies, file)
```
 ## Начало работы
- **Вам потребуется настроенный аккаунт [Telegram](https://core.telegram.org/bots) для получения уведомлений и [Docker](https://www.docker.com/) для запуска контейнера.**

```bash
# Клонирование репозитория
git clone https://github.com/YourGithubProfile/FON_BET_SCANNER.git

# Windows. Откройте сценарий
docker_activate.bat
```


