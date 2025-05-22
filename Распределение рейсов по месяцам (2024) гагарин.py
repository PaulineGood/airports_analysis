import psycopg2
import matplotlib.pyplot as plt
import matplotlib
import datetime
import numpy as np
from matplotlib.colors import LinearSegmentedColormap

# Устанавливаем шрифт с поддержкой кириллицы
matplotlib.rcParams['font.family'] = 'DejaVu Sans'

# Соединение с БД
conn = psycopg2.connect(
    dbname="gagarin",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Получаем все периоды из таблицы flights
cursor.execute("SELECT period FROM flights")
periods = cursor.fetchall()

# Словарь для подсчёта рейсов по месяцам
flights_per_month = {i: 0 for i in range(1, 13)}

# Словарь для перевода месяцев
month_map = {
    "янв": 1, "фев": 2, "мар": 3, "апр": 4, "май": 5, "мая": 5, "июн": 6,
    "июл": 7, "авг": 8, "сен": 9, "окт": 10, "ноя": 11, "дек": 12
}

def parse_period(period_str):
    if not period_str or '/' not in period_str:
        return None, None
    start_str, end_str = [x.strip() for x in period_str.split('/')]
    
    def parse_date(d):
        parts = d.split()
        day = parts[0]
        mon = parts[1].lower()
        return datetime.date(2024, month_map[mon[:3]], int(day))
    
    return parse_date(start_str), parse_date(end_str)

# Подсчёт рейсов
for (period,) in periods:
    start_date, end_date = parse_period(period)
    if start_date and end_date:
        current = start_date
        while current <= end_date:
            flights_per_month[current.month] += 1
            current += datetime.timedelta(days=1)

# Подготовка данных
months = ['янв', 'фев', 'мар', 'апр', 'май', 'июн', 'июл', 'авг', 'сен', 'окт', 'ноя', 'дек']
values = list(flights_per_month.values())
indices = list(flights_per_month.keys())

# Градиентная цветовая карта
cmap = LinearSegmentedColormap.from_list("gradient", ["#ffd1dc", "#ff4d4d"])
colors = [cmap(i / max(values)) for i in values]

# Построение графика
plt.figure(figsize=(10, 6))
bars = plt.bar(indices, values, color=colors)

# Подписи
plt.xlabel('Месяц')
plt.ylabel('Количество рейсов')
plt.title('Распределение рейсов по месяцам (2024)')
plt.xticks(indices, months)
plt.tight_layout()

# Сохранение и отображение
plt.savefig("flights_per_month.png")
plt.show()

cursor.close()
conn.close()
