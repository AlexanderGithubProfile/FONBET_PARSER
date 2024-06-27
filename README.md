# FON BET SCANNER: Advanced Betting Alert System
- Удобный парсер для отслеживания событий на динамическом сайте, с обходом обнаружения автоматизации, работой без окна и уведомлениями в реальном времени.

[English](./README_en.md) | [Русский](./README.md)

<p align="left">
 <img src="img/01_fon_bet_scanner_1.png" width="400">
 <img src="img/01_fon_bet_scanner_2.png" width="400">
</p>

## Использование 
Приложение в контейнере работает без окна браузера, включение исполняемым файлом для удобной работы без IDE (pycharm) и авто-запуском докера
> - **автоматизация управления**: управление запуском и остановкой парсера из чата, подгрузка данных входа через куки
> - **парсинг контента**: скрипт имитирует поведение пользователя, скроллит страницу и собирает необходимые данные
> - **режим полной автоматизации**: расчет ставок и их выставление на основе собранных данных
> - **отправка скриншотов в Telegram**: скрипт может делать скриншоты текущего экрана и отправлять их в чат
> - **статистика по счету**: возможность получения данных по текущему состоянию счета и сделкам
> - **блокировка рекламы**: скрипт автоматически закрывает всплывающие окна и рекламу

## Применяемые технологии
Скрипт выполнен с использованием следующих технологий и библиотек:
> - **[Xvfb](https://www.x.org/releases/X11R7.6/doc/man/man1/Xvfb.1.xhtml)**: виртуальный X-сервер, обеспечивающий работу headless-браузера
> - **[fluxbox](https://fluxbox.org/)**: легковесный оконный менеджер для управления виртуальными окнами.
> - **[x11vnc](https://www.karlrunge.com/x11vnc/)**: VNC-сервер для удаленного управления виртуальными окнами.
> - **[OpenCV](https://opencv.org/)**: библиотека для обработки изображений, используемая для работы со скриншотами.
> - **[selenium + uc](https://www.selenium.dev/)**: средство для автоматизации веб-браузеров.
> - **[beautifulsoup4](https://www.crummy.com/software/BeautifulSoup/)**: библиотека для парсинга HTML и XML.
> - **[requests](https://docs.python-requests.org/en/latest/)**: библиотека для HTTP-запросов.
> - **[docker](https://www.docker.com/)**: платформа для разработки и доставки приложений в контейнерах.
> - **[telebot](https://pypi.org/project/pyTelegramBotAPI/)**: библиотека для работы с API Telegram.
> - **[pandas](https://pandas.pydata.org/)**: библиотека для работы с данными.
> - **[time](https://docs.python.org/3/library/time.html)**: библиотека для работы с временем.
> - **[logging](https://docs.python.org/3/library/logging.html)**: библиотека для ведения логов.

<p align="left">
   <img src="img/02_fon_bet_scanner_1.png" width="400">
   <img src="img/02_fon_bet_scanner_2.png" width="400">
</p>

## Организация проекта

1. **fon_bet_scanner**: основной каталог проекта и настройки приложения.

    - `Dockerfile`: настройки Docker контейнера.
    - `README.md`: файл с описанием проекта.
    - `docker-compose.yml`: конфигурация для Docker Compose.
    - `docker_activate.bat`: сценарий для активации Docker в Windows.
    - `entrypoint.sh`: сценарий для запуска контейнера.
    - `mount`: директория с основными скриптами и данными.
        - `bot_telegram.py`: скрипт для взаимодействия с Telegram.
        - `cookies.json`: файл с куками для входа.
        - `main.py`: основной файл запуска скрипта.
        - `run_background.py`: скрипт для фонового выполнения задач.
        - `utils_db.py`: вспомогательные функции для работы с базой данных.
        - `utils_img.py`: вспомогательные функции для работы с изображениями.
        - `utils_navigation.py`: вспомогательные функции для навигации по сайту.
        - `utils_processsing.py`: вспомогательные функции для обработки данных.
        - `utils_telegram.py`: вспомогательные функции для работы с Telegram.
    - `requirements.txt`: список зависимостей проекта.
      
## Создайте файл .env для настройки переменных окружения:
```dotenv 
TELEGRAM_TOKEN=        # telegram_bot_token
CHAT_ID=               # telegram_chat_id
MIN_BET=               # минимальная_ставка
GAME_MINUTES=          # время_игры
MAX_BET=               # максимальная_ставка
SCORE=                 # начальный_счет
```


## Начало работы
- **Вам потребуется настроенный аккаунт [Telegram](https://core.telegram.org/bots) для получения уведомлений и [Docker](https://www.docker.com/) для запуска контейнера.**

```bash
# Клонирование репозитория
git clone https://github.com/YourGithubProfile/FON_BET_SCANNER.git
```
 **Откройте сценарий для активации Docker в Windows.**
```bash
# Windows. Откройте сценарий
docker_activate.bat
```

