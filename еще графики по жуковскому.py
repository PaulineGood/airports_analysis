import psycopg2
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap
from datetime import datetime
from collections import Counter

def get_gradient_colors(values, color_start, color_end):
    max_val = max(values) if values else 0
    cmap = LinearSegmentedColormap.from_list("custom_grad", [color_start, color_end])
    if max_val == 0:
        return ['#cccccc'] * len(values)
    return [cmap(v / max_val) for v in values]

# Подключение к БД
conn = psycopg2.connect(
    dbname="gagarin",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("SELECT date FROM zhukovsky_flights")
rows = cursor.fetchall()

dates = []
for (date_str,) in rows:
    try:
        # Парсим строку "дд.мм.гггг"
        dt = datetime.strptime(date_str, "%d.%m.%Y")
        dates.append(dt)
    except Exception as e:
        # Если есть некорректные данные, можно пропускать
        continue

# Считаем количество по дням недели
days = ['Пн', 'Вт', 'Ср', 'Чт', 'Пт', 'Сб', 'Вс']
day_counts_dict = Counter([days[dt.weekday()] for dt in dates])
day_counts = [day_counts_dict.get(day, 0) for day in days]

colors_day = get_gradient_colors(day_counts, "#ffb3ba", "#ff1a1a")

plt.figure(figsize=(10, 6))
bars = plt.bar(days, day_counts, color=colors_day)
plt.title("Распределение рейсов по дням недели (Жуковский)")
plt.xlabel("День недели")
plt.ylabel("Количество рейсов")
for bar, count in zip(bars, day_counts):
    plt.text(bar.get_x() + bar.get_width()/2, count + 0.5, str(count), ha='center')
plt.tight_layout()
plt.savefig("zhukovsky_flights_by_day.png")
plt.close()

# Считаем количество по месяцам
months = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июн',
          'Июл', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
month_counts_dict = Counter([dt.month for dt in dates])
month_counts = [month_counts_dict.get(i+1, 0) for i in range(12)]

colors_month = get_gradient_colors(month_counts, "#bae1ff", "#0059b3")

plt.figure(figsize=(12, 6))
bars = plt.bar(months, month_counts, color=colors_month)
plt.title("Распределение рейсов по месяцам (Жуковский)")
plt.xlabel("Месяц")
plt.ylabel("Количество рейсов")
for bar, count in zip(bars, month_counts):
    plt.text(bar.get_x() + bar.get_width()/2, count + 0.5, str(count), ha='center')
plt.tight_layout()
plt.savefig("zhukovsky_flights_by_month.png")
plt.close()

# Считаем количество по годам
years_list = sorted(set(dt.year for dt in dates))
year_counts_dict = Counter([dt.year for dt in dates])
year_counts = [year_counts_dict.get(year, 0) for year in years_list]

colors_year = get_gradient_colors(year_counts, "#b2fab4", "#2f8f2f")

plt.figure(figsize=(12, 6))
bars = plt.bar([str(y) for y in years_list], year_counts, color=colors_year)
plt.title("Распределение рейсов по годам (Жуковский)")
plt.xlabel("Год")
plt.ylabel("Количество рейсов")
for bar, count in zip(bars, year_counts):
    plt.text(bar.get_x() + bar.get_width()/2, count + 0.5, str(count), ha='center')
plt.tight_layout()
plt.savefig("zhukovsky_flights_by_year.png")
plt.close()

cursor.close()
conn.close()
print("Три графика сохранены: по дням, месяцам и годам.")
