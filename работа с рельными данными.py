import json
from datetime import datetime, timedelta

def replace_russian_months(date_str):
    months = {
        "янв": "January", "фев": "February", "мар": "March", "апр": "April",
        "мая": "May", "июн": "June", "июл": "July", "авг": "August",
        "сен": "September", "окт": "October", "ноя": "November", "дек": "December",
        "января": "January", "февраля": "February", "марта": "March", "апреля": "April",
        "июня": "June", "июля": "July", "августа": "August",
        "сентября": "September", "октября": "October", "ноября": "November", "декабря": "December"
    }
    for ru, en in months.items():
        date_str = date_str.replace(ru, en)
    return date_str


# Словарь преобразования сокращений дней недели в номера (понедельник=0, воскресенье=6)
day_mapping = {
    'пн': 0, 'вт': 1, 'ср': 2, 'чт': 3, 'пт': 4, 'сб': 5, 'вс': 6
}

def parse_period(period_str):
    start_str, end_str = period_str.split('/')
    start_str = replace_russian_months(start_str.replace('\xa0', ' ').strip())
    end_str = replace_russian_months(end_str.replace('\xa0', ' ').strip())
    start = datetime.strptime(start_str + ' 2025', "%d %B %Y")
    end = datetime.strptime(end_str + ' 2025', "%d %B %Y")
    return start, end


def expand_flight(entry):
    start_date, end_date = parse_period(entry["Период"])
    days_str = entry["Дни полетов"].strip().lower()

    if days_str == "ежедневно":
        weekdays = list(range(7))  # Понедельник (0) – Воскресенье (6)
    else:
        day_mapping = {
            'пн': 0, 'вт': 1, 'ср': 2, 'чт': 3, 'пт': 4, 'сб': 5, 'вс': 6
        }
        weekdays = [day_mapping[day.strip()] for day in days_str.split(',')]

    result = []
    current = start_date
    while current <= end_date:
        if current.weekday() in weekdays:
            new_entry = entry.copy()
            new_entry["Дата рейса"] = current.strftime("%Y-%m-%d")
            result.append(new_entry)
        current += timedelta(days=1)
    return result


# === Основной процесс ===

with open("schedule.json", "r", encoding="utf-8") as f:
    raw_data = json.load(f)

# Обработка может быть как списком, так и одним словарем
if isinstance(raw_data, dict):
    raw_data = [raw_data]

expanded_data = []
for flight in raw_data:
    expanded_data.extend(expand_flight(flight))

# Сохраняем в новый JSON
with open("expanded_schedule.json", "w", encoding="utf-8") as f:
    json.dump(expanded_data, f, ensure_ascii=False, indent=2)

print(f"✅ Создан файл expanded_schedule.json с {len(expanded_data)} рейсами.")
