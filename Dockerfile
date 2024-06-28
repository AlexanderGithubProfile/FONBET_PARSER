# Основа - Ubuntu 22.04
FROM debian:bullseye

# Порт сервера VNC
EXPOSE 5900

# Устанавливаем часовой пояс, чтобы tzdata не запрашивал его
ENV DEBIAN_FRONTEND=noninteractive

# Установка зависимостей
RUN apt-get update && apt-get install -y \
    python3 \
    python3-venv \
    python3-pip \
    xvfb \
    fluxbox \
    x11vnc \
    x11-apps \
    sudo \
    wget \
    curl \
    htop

# Инит и активация виртуальной среды
RUN python3 -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Установка requirements и обновление pip
RUN apt-get update && apt-get install -y libpq-dev build-essential
COPY requirements.txt /requirements.txt
RUN pip install --upgrade pip

# Установка продуктовых зависимостей
RUN pip install --no-cache-dir -r /requirements.txt
RUN pip install ipython
RUN pip install undetected-chromedriver

# Добавление репозитория Google Chrome и установка Chrome
RUN echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | gpg --dearmor > /etc/apt/trusted.gpg.d/google-chrome.gpg
RUN apt-get update && apt-get install google-chrome-stable=126.* -y

# Копирование entrypoint.sh в корневую директорию контейнера и делаем entrypoint скрипт исполняемым
COPY entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Устанавливаем точку входа
ENTRYPOINT ["/entrypoint.sh"]