#!/usr/bin/env bash
# Инициализируем DISPLAY, указываем номер и удаляем файл блокировки /tmp/.X0-lock,
export DISPLAY=:0
rm -f /tmp/.X0-lock

# Загрузка виртуального X-сервера (Xvfb)
Xvfb -ac -screen 0 1920x1080x24 &
echo -e "### Старт виртуального X-сервера (Xvfb)"

# Загрузка оконного менеджера (fluxbox)
fluxbox -screen 0 &> /dev/null &
echo -e "### Старт оконного менеджера (fluxbox)"

# Загрузка VNC-сервера (x11vnc)
x11vnc -passwd ${VNC_PASSWORD:-password} -N -forever -rfbport 5900 &> /dev/null &
echo -e "### Старт VNC-сервера (x11vnc)"

cd /opt/wd

# Запуск
echo -e "### Старт telegram-бота"
"$@"

# Ожидание завершения всех фоновых процессов
echo -e "\n### Завершено"
wait
