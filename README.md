# EGE-Writing-Autograde-Bot

## Описание

Этот Телеграм-бот создан для помощи в подготовке к ЕГЭ по английскому языку. Он анализирует и проверяет электронные письма, предоставляет оценки по критериям и дает рекомендации по улучшению.

## Основные функции

- Оценка текстов по критериям.
- Выявление ошибок и предоставление рекомендаций по их исправлению.
- Предоставление статистики для отслеживания прогресса.

## Интеграция с FastAPI

Бот является частью общего проекта AutoGrade-ENG-Writing, он обращается к серверу autograde_api с предсказательной моделью и получает в качестве результата анализ и оценку текста.

## Инструкция по запуску

Для запуска Телеграм-бота отдельно необходимо выполнить следующие шаги:

Шаг 1: Клонирование репозитория
Склонируйте репозиторий на свой локальный компьютер с помощью команды git clone:
```
git clone https://github.com/AlbinaBurlova/EGE-Writing-Autograde-Bot.git
```
Шаг 2: Настройка переменных окружения
Создайте файл .env в корневом каталоге проекта и добавьте следующие переменные:

    
    BOT_TOKEN=ваш_токен_бота
    DEVELOPER_ID_1=telegram_id_1
    DEVELOPER_ID_2=telegram_id_2
    API_ADDRESS=адрес_вашего_api
    

Замените `ваш_токен_бота`, `telegram_id_1`, `telegram_id_2` и `адрес_вашего_api` на реальные значения.

Шаг 3: Сборка и запуск Docker контейнера
Перейдите в корневой каталог проекта и выполните следующую команду для сборки и запуска Docker контейнера:
 ```
docker build -t ege-bot .
docker run -d --name ege-bot ege-bot
 ```

Дополнительно. Если вы планируете запускать бота на сервере PythonAnywhere, добавьте следующий код в файл bot.py:

    
    from aiogram.client.session.aiohttp import AiohttpSession
    
    session = AiohttpSession(proxy='http://proxy.server:3128')

    bot = Bot(token=config.bot_token.get_secret_value(),
              parse_mode="HTML", session=session)
    
    
После выполнения этих шагов бот должен быть успешно запущен и готов к использованию.

