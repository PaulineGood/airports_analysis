import psycopg2
import matplotlib.pyplot as plt
import matplotlib
import datetime
from matplotlib.colors import LinearSegmentedColormap

matplotlib.rcParams['font.family'] = 'DejaVu Sans'

conn = psycopg2.connect(
    dbname="gagarin",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

cursor.execute("SELECT schedule_date FROM flights")
dates = cursor.fetchall()

flights_per_year = {}

for (date_val,) in dates:
    try:
        if isinstance(date_val, datetime.date):
            year = date_val.year
        else:
            # Попытка распарсить строку
            year = int(str(date_val)[:4])
        flights_per_year[year] = flights_per_year.get(year, 0) + 1
    except (ValueError, TypeError):
        # Пропускаем некорректные значения
        continue

years = sorted(flights_per_year.keys())
values = [flights_per_year[year] for year in years]

cmap = LinearSegmentedColormap.from_list("gradient_years", ["#b2fab4", "#2f8f2f"])
colors = [cmap(v / max(values)) for v in values]

plt.figure(figsize=(10, 6))
bars = plt.bar(years, values, color=colors)

plt.xlabel('Год')
plt.ylabel('Количество рейсов')
plt.title('Распределение рейсов по годам')
plt.xticks(years)
plt.tight_layout()

for bar, count in zip(bars, values):
    plt.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 2, str(count), ha='center', va='bottom')

plt.savefig("flights_per_year.png")
plt.show()

cursor.close()
conn.close()
