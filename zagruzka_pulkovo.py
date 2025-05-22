import json
import psycopg2

# Подключение к БД
conn = psycopg2.connect(
    dbname="gagarin",
    user="postgres",
    password="1",
    host="localhost",
    port="5432"
)
cursor = conn.cursor()

# Создаем таблицу (если еще не создана)
cursor.execute("""
CREATE TABLE IF NOT EXISTS spb_flights (
    id SERIAL PRIMARY KEY,
    departure_time TEXT,
    days_of_week TEXT[],
    airline TEXT,
    flight_number TEXT,
    aircraft_type TEXT
)
""")
conn.commit()

# Чтение JSON-файла
with open("SPB_comb.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# Вставка данных
for record in data:
    cursor.execute("""
        INSERT INTO spb_flights (departure_time, days_of_week, airline, flight_number, aircraft_type)
        VALUES (%s, %s, %s, %s, %s)
    """, (
        record.get("Отправление"),
        record.get("Дни полетов"),
        record.get("Авиакомпания"),
        record.get("Номер рейса"),
        record.get("Тип судна")
    ))

conn.commit()
cursor.close()
conn.close()

print("Данные из SPB_comb.json успешно загружены в таблицу spb_flights.")
