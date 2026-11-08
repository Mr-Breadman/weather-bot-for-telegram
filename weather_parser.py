import requests
from bs4 import BeautifulSoup
import lxml

BASE_URL = "https://world-weather.ru/pogoda/"

CITIES = {
    "🇧🇾 Беларусь": {
        "минск": "belarus/minsk",
        "гомель": "belarus/gomel",
        "брест": "belarus/brest",
        "витебск": "belarus/vitebsk",
        "гродно": "belarus/grodno",
        "могилев": "belarus/mogilev",
    },
    "🇷🇺 Россия": {
        "москва": "russia/moscow",
        "санкт-петербург": "russia/saint_petersburg",
        "питер": "russia/saint_petersburg",
        "новосибирск": "russia/novosibirsk",
        "екатеринбург": "russia/yekaterinburg",
        "казань": "russia/kazan",
    },
    "🇺🇦 Украина": {
        "киев": "ukraine/kiev",
        "харьков": "ukraine/kharkiv",
        "одесса": "ukraine/odessa",
    }
}

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.5,en;q=0.3",
    "Referer": "https://world-weather.ru/",
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
}


def get_weather(city):
    city = city.lower().strip().replace("ё", "е")

    city_slug = None
    for country_cities in CITIES.values():
        if city in country_cities:
            city_slug = country_cities[city]
            break

    if not city_slug:
        return ("Упс, я не нашел такой город!\n"
                " Возможно его нет в списке. Если он все же есть, попробуйте повторить позже.")


    url = BASE_URL + city_slug + "/"
    response = requests.get(url, headers=HEADERS)

    print(f"status: {response.status_code}")

    if response.status_code != 200:
        return f"Error {response.status_code}: unable to enter to website"

    soup = BeautifulSoup(response.text, "lxml")
    temp_tag = soup.find('div', id='weather-now-number')
    desc_temp = soup.find('div', class_='hourly-summary')

    if not temp_tag:
        return "Не получилось найти температуру, попробуйте позже"

    temp = temp_tag.text.strip()
    desc = desc_temp.text.strip() if desc_temp else ""


    result = f"🌤️ <b>Погода в городе {city.capitalize()}</b>\n\n🌡️ Температура: <b>{temp}C</b>"
    if desc:
        result += f"\n\n {desc}"

    return result



def get_supported_cities():
    lines = []
    for country, cities in CITIES.items():
        unique_cities = sorted(set(cities.keys()))
        cities_str = ", ".join(c.capitalize() for c in unique_cities)
        lines.append(f"<b>{country}</b>\n{cities_str}")
    return "\n\n".join(lines)

def get_week_forecast(city):
    city = city.lower().strip().replace("ё", "е")

    city_slug = None
    for country_cities in CITIES.values():
        if city in country_cities:
            city_slug = country_cities[city]
            break

    if not city_slug:
        return "🤔 Я не знаю такой город."

    url = BASE_URL + city_slug + "/"
    response = requests.get(url, headers=HEADERS)

    if response.status_code != 200:
        return f"⚠️ Ошибка {response.status_code}: сайт не пустил. Повторите позже."

    soup = BeautifulSoup(response.text, "lxml")
    days = soup.find_all('li', class_='tab-w')

    if not days:
        return "Прогноз не найден"

    result = f"📅 <b>Прогноз на 10 дней для города {city.capitalize()}:</b>\n\n"

    for day in days:
        day_name = day.find('div', class_='day-week')
        day_name = day_name.text.strip() if day_name else '?'

        day_num = day.find('div', class_='numbers-month')
        day_num = day_num.text.strip() if day_num else '?'

        month = day.find('div', class_='month')
        month = month.text.strip() if month else ''

        icon = day.find('span', class_='icon-weather')
        description = icon.get('title') if icon else 'нет данных'

        temp_day = day.find('div', class_='day-temperature')
        temp_night = day.find('div', class_='night-temperature')

        temp_day = temp_day.text.strip() if temp_day else '?'
        temp_night = temp_night.text.strip() if temp_night else '?'

        desc_lower = description.lower()

        if "ясно" in desc_lower or "солнечно" in desc_lower:
            emoji = "☀️"
        elif "дождь" in desc_lower or "ливень" in desc_lower:
            emoji = "🌧️"
        elif "снег" in desc_lower:
            emoji = "🌨️"
        elif "гроза" in desc_lower:
            emoji = "⛈️"
        elif "пасмурно" in desc_lower:
            emoji = "☁️"
        elif "облачно" in desc_lower or "облачность" in desc_lower:
            emoji = "⛅"
        elif "туман" in desc_lower:
            emoji = "🌫️"
        else:
            emoji = "☁️"

        result += (
            f"<b>{day_name}, {day_num} {month}</b>\n"
            f"🌡️ Днём: {temp_day} | Ночью: {temp_night}\n"
            f"{emoji} {description}\n\n"
        )

    return result

if __name__ == "__main__":
    print(get_weather("Минск"))





