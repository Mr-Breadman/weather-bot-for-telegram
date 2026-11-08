import aiogram
import asyncio
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message
from datetime import datetime
from data import init_db, add_user, get_users_by_time, remove_user
from config import TOKEN
import re


from weather_parser import get_weather, get_supported_cities, get_week_forecast
logging.basicConfig(level=logging.INFO)


init_db()
bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: Message):
    await message.answer("👋Привет! Я бот погоды. Напиши /weather {название города}, чтобы узнать погоду!")

@dp.message(Command('help'))
async def cmd_help(message: Message):
    cities_text = get_supported_cities()
    await message.answer("Вот что я умею:\n\n"
                         "<code>/start</code> — начать работу\n\n"
                         "<code>/help</code> — показать это сообщение\n\n"
                         "<code>/weather {название города}</code> — погода в выбранном городе\n"
                         "<code>/week {название города}</code> — прогноз на ближайшие 10 дней\n"
                         "<code>/subscribe {название города} {время}</code> — Каждый день бот будет отправлять текущую погоду для введенного города.\n"
                         "<code>/unsubscribe</code> — отключиться от рассылки\n\n"
                         f"<b>Поддерживаемые города:</b>\n{cities_text}",
                         parse_mode="HTML"
                         )

@dp.message(Command('weather'))
async def cmd_wather(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args) < 2:
        await message.answer("Напиши город: /weather Минск")
        return

    city = args[1]
    weather = get_weather(city)
    await message.answer(weather, parse_mode="HTML")


async def send_daily_weather():
    now=datetime.now().strftime("%H:%M")
    print(f"проверяю расписание на {now}...")

    users = get_users_by_time(now)

    for user_id, city in users:
        weather = get_weather(city)
        try:
            await bot.send_message(chat_id=user_id, text=weather, parse_mode="HTML")
            print(f" Отправлено пользователю {user_id}")
        except Exception as e:
            print(f" Ошибка отправки {user_id}: {e}")



@dp.message(Command('week'))
async def cmd_week(message: Message):
    args = message.text.split(maxsplit=1)

    if len(args)<2:
        await message.answer(
            "Ты не указал город.\n"
            "Например: <code>/week Минск</code>",
            parse_mode="HTML")
        return

    city = args[1]

    await message.answer("⏳ Собираю прогноз на 10 дней...")
    forecast = get_week_forecast(city)
    await message.answer(forecast, parse_mode='HTML')


@dp.message(Command('subscribe'))
async def cmd_sub(message: Message):
    args = message.text.split(maxsplit = 2)

    if len(args) < 3:
        await message.answer(
            "Похоже, ты не написал город или время.\n"
            "попробуй еще раз (Например: <code>/subscribe Минск 08:00</code>",
            parse_mode="HTML"
        )
        return

    city = args[1]
    time_str = args[2]

    if not re.match(r"^\d{2}:\d{2}$", time_str):
        await message.answer("Время должно быть в формате ЧЧ:ММ (например, 08:00)")
        return

    test_weather = get_weather(city)
    if "не знаю такой город" in test_weather:
        await message.answer("Я пока не знаю такой город. Посмотри список в /help.")
        return

    user_id = message.from_user.id
    add_user(user_id, city.lower(), time_str)

    await message.answer(
        f" Отлично! Теперь я буду присылать тебе погоду для города <b>{city.capitalize()}</b> каждый день в <b>{time_str}</b>.",
        parse_mode="HTML"
    )


@dp.message(Command("unsubscribe"))
async def cmd_unsub(message: Message):
    user_id = message.from_user.id
    if remove_user(user_id):
        await message.answer(
            "Ты успешно отписался от ежедневной рассылки погоды. Если захочешь вернуться — просто напиши /subscribe.")
    else:
        await message.answer(
            "Ты и так не был подписан на рассылку.\nНапиши <code>/subscribe Минск 08:00</code>, чтобы подписаться.",
            parse_mode="HTML")


async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
    scheduler.add_job(send_daily_weather, 'cron', second=0)
    scheduler.start()
    print('планировщик запущен.')

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())

