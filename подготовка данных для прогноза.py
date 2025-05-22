import json
from datetime import datetime, timedelta
import re

# Соответствие дней недели
weekday_map = {
    "пн": 0, "вт": 1, "ср": 2, "чт": 3,
    "пт": 4, "сб": 5, "вс": 6
}

# Словарь направлений по кодам аэропортов
airport_names = {
    'VKO': 'Внуково',
    'SGC': 'Сургут',
    'SVO': 'Шереметьево',
    'DME': 'Домодедово',
    'AYT': 'Анталия',
    'AER': 'Сочи (Адлер)',
    'SIP': 'Симферополь',
    'LED': 'Пулково',
    'SVX': 'Кольцово (Екатеринбург)',
    'KRR': 'Пашковский (Краснодар)',
    'GOI': 'Даболим (Гоа, Индия)',
    'MRV': 'Минеральные Воды',
    'ROV': 'Платов (Ростов-на-Дону)',
    'KZN': 'Казань',
    'AAQ': 'Анапа',
    'OVB': 'Толмачёво (Новосибирск)',
    'UFA': 'Уфа',
    'TJM': 'Рощино (Тюмень)',
    'EVN': 'Звартноц (Ереван, Армения)',
    'PFO': 'Пафос (Кипр)',
    'GYD': 'Гейдар Алиев (Баку, Азербайджан)',
    'SKG': 'Македония (Салоники, Греция)',
    'FEG': 'Фергана (Узбекистан)',
    'NUX': 'Новый Уренгой',
    'NBE': 'Энфида (Тунис)',
    'FRU': 'Манас (Бишкек, Кыргызстан)',
    'SSH': 'Шарм-эль-Шейх (Египет)',
    'MCX': 'Уйташ (Махачкала)',
    'DYU': 'Душанбе (Таджикистан)',
    'KGD': 'Храброво (Калининград)',
    'LBD': 'Худжанд (Таджикистан)',
    'KUF': 'Курумоч (Самара)',
    'HRG': 'Хургада (Египет)',
    'GRV': 'Грозный',
    'ZIA': 'Жуковский',
    'GOJ': 'Нижний Новгород',
    'KQT': 'Бохтар (Таджикистан)',
    'TJU': 'Куляб (Таджикистан)',
    'OSS': 'Ош (Кыргызстан)'
}

# Функция для преобразования строки "21 авг / 16 сен" в даты
def parse_period(period_str, year=2019):
    parts = re.split(r'/|–|-', period_str)
    if len(parts) != 2:
        return None, None
    start_str, end_str = parts[0].strip(), parts[1].strip()

    months = {
        "янв": 1, "фев": 2, "мар": 3, "апр": 4,
        "мая": 5, "май": 5, "июн": 6, "июл": 7,
        "авг": 8, "сен": 9, "окт": 10, "ноя": 11, "дек": 12
    }

    def parse_date(s):
        day, mon = s.split()
        return datetime(year, months[mon], int(day))

    start_date = parse_date(start_str)
    end_date = parse_date(end_str)
    if end_date < start_date:
        end_date = end_date.replace(year=year + 1)
    return start_date, end_date

# Читаем исходный файл
with open('all_flights.json', 'r', encoding='utf-8') as f:
    flights = json.load(f)

result = []

for flight in flights:
    days = flight["Дни полетов"]
    if isinstance(days, list):
        flight_days = [weekday_map[d] for d in days]
        days_str = ", ".join(days)
    else:
        continue  # если не список — пропускаем

    period = flight.get("Период", "").strip()
    date_raw = flight.get("Дата расписания", "")
    try:
        year = int(date_raw[:4])
    except ValueError:
        continue  # пропускаем записи с некорректной датой

    start_date, end_date = parse_period(period, year=year)

    if not start_date or not end_date:
        continue  # если не удалось распарсить период — пропускаем

    airport_code = flight.get("Аэропорт", "").strip()
    direction = airport_names.get(airport_code, "неизвестно")

    current = start_date
    while current <= end_date:
        if current.weekday() in flight_days:
            result.append({
                "Направление": direction,
                "Отправление": flight["Отправление"],
                "Прибытие": flight["Прибытие"],
                "Дни полетов": days_str,
                "Период": period,
                "Авиакомпания": flight["Авиакомпания"],
                "№ Рейса": flight["Номер рейса"],
                "Тип судна": flight["Тип судна"],
                "Аэропорт": airport_code,
                "Дата рейса": current.strftime('%Y-%m-%d')
            })
        current += timedelta(days=1)

# Сохраняем результат
with open('all_flights_by_date.json', 'w', encoding='utf-8') as f_out:
    json.dump(result, f_out, ensure_ascii=False, indent=4)

print(f"Готово! Создано записей: {len(result)}")
