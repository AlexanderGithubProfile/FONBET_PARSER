@echo off
:: Проверка, запущен ли Docker
echo Checking if Docker is running...
docker info >nul 2>&1
if ERRORLEVEL 1 (
    echo Docker is not running. Starting Docker...
    start "" "%PROGRAMFILES%\Docker\Docker\Docker Desktop.exe"
    :: Ожидание запуска Docker
    timeout /t 20
)

:: Запуск docker-compose
echo Starting docker-compose...
docker-compose up