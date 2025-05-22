import psycopg2
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Подключение к БД
conn = psycopg2.connect(
    dbname="gagarin",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# ---------- ГРАФИК 1: По авиакомпаниям ----------
cursor.execute("""
    SELECT airline, COUNT(*) FROM zhukovsky_flights
    GROUP BY airline ORDER BY COUNT(*) DESC
""")
airline_data = cursor.fetchall()

airlines = [row[0] for row in airline_data]
counts = [row[1] for row in airline_data]

colors = cm.Blues(np.linspace(0.4, 0.9, len(counts)))

plt.figure(figsize=(10, 6))
bars = plt.barh(airlines, counts, color=colors)
plt.xlabel('Количество рейсов', fontsize=12)
plt.ylabel('Авиакомпания', fontsize=12)
plt.title('Распределение рейсов по авиакомпаниям', fontsize=14, weight='bold')

for bar, count in zip(bars, counts):
    plt.text(count + 0.5, bar.get_y() + bar.get_height()/2, str(count),
             va='center', fontsize=10)

plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("flights_by_airline.png", dpi=300)
print("График 1 сохранен как flights_by_airline.png")

# ---------- ГРАФИК 2: По направлениям ----------
cursor.execute("""
    SELECT destination, COUNT(*) FROM zhukovsky_flights
    GROUP BY destination ORDER BY COUNT(*) DESC
""")
destination_data = cursor.fetchall()

destinations = [row[0] for row in destination_data]
dest_counts = [row[1] for row in destination_data]

colors = cm.Greens(np.linspace(0.4, 0.9, len(dest_counts)))

plt.figure(figsize=(10, 6))
bars = plt.barh(destinations, dest_counts, color=colors)
plt.xlabel('Количество рейсов', fontsize=12)
plt.ylabel('Аэропорт назначения', fontsize=12)
plt.title('Распределение рейсов по направлениям', fontsize=14, weight='bold')

for bar, count in zip(bars, dest_counts):
    plt.text(count + 0.5, bar.get_y() + bar.get_height()/2, str(count),
             va='center', fontsize=10)

plt.gca().invert_yaxis()
plt.grid(axis='x', linestyle='--', alpha=0.5)
plt.tight_layout()
plt.savefig("flights_by_destination.png", dpi=300)
print("График 2 сохранен как flights_by_destination.png")

# Завершение работы
cursor.close()
conn.close()
