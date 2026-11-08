# Weather Telegram Bot 🌤️

Асинхронный Telegram-бот на `aiogram 3`, который присылает текущую погоду и прогноз на 10 дней, а также делает ежедневную рассылку по расписанию.

## Функционал
- `/weather [город]` — текущая погода (температура, описание)
- `/week [город]` — прогноз на 10 дней
- `/subscribe [город] [время]` — подписка на ежедневную рассылку (например, `/subscribe Москва 08:00`)
- `/unsubscribe` — отписка от рассылки
- `/help` — список команд и доступных городов

## Технологии
- **aiogram 3** (асинхронный Telegram API)
- **BeautifulSoup4 + requests** (парсинг сайта world-weather.ru)
- **SQLite3** (хранение подписчиков и времени)
- **APScheduler** (запуск рассылки по расписанию)
- Динамические эмодзи в зависимости от погоды.

## Установка и запуск

1. Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Mr-Breadman/weather-bot-for-telegram.git
2. Установите зависимости:
   pip install -r requirements.txt
3. Получите токен бота у @BotFather в Telegram.
4. Переименуйте файл config_example.py в config.py и вставьте туда ваш токен:
   BOT_TOKEN = "ВАШ_ТОКЕН_ЗДЕСЬ"
5. Запустите бота:
   python bot.py
 
