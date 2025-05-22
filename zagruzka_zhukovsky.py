import psycopg2
import json
from datetime import datetime

def create_connection():
    return psycopg2.connect(
        host="localhost",
        database="gagarin",
        user="postgres",
        password="1"
    )

def create_table(conn):
    with conn.cursor() as cursor:
        cursor.execute('''
        DROP TABLE IF EXISTS zhukovsky_flights;

        CREATE TABLE zhukovsky_flights (
            id SERIAL PRIMARY KEY,
            flight_number TEXT,
            destination TEXT,
            airline TEXT,
            date TEXT,
            time TEXT,
            time_text TEXT,
            status TEXT,
            day_of_week TEXT,
            day_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        conn.commit()
        print("✅ Таблица zhukovsky_flights успешно создана!")

def load_data(conn, json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with conn.cursor() as cursor:
        for flight in data:
            try:
                cursor.execute('''
                INSERT INTO zhukovsky_flights (
                    flight_number, destination, airline,
                    date, time, time_text, status,
                    day_of_week, day_code
                ) VALUES (
                    %(flight_number)s, %(destination)s, %(airline)s,
                    %(date)s, %(time)s, %(time_text)s, %(status)s,
                    %(day_of_week)s, %(day_code)s
                );
                ''', {
                    'flight_number': flight.get('flight_number', ''),
                    'destination': flight.get('destination', ''),
                    'airline': flight.get('airline', ''),
                    'date': flight.get('date', ''),
                    'time': flight.get('time', ''),
                    'time_text': flight.get('time_text', ''),
                    'status': flight.get('status', ''),
                    'day_of_week': flight.get('day_of_week', ''),
                    'day_code': flight.get('day_code', '')
                })
            except Exception as e:
                print(f"❌ Ошибка при вставке записи: {flight}")
                print(f"Текст ошибки: {e}")

        conn.commit()
        print(f"✅ Успешно загружено {len(data)} записей!")

# Основной блок
try:
    conn = create_connection()
    create_table(conn)
    load_data(conn, "C:/Users/Alina/Desktop/pytonchek/zhukovsky_flights_with_weekdays.json")
except Exception as e:
    print(f"❌ Произошла ошибка: {e}")
finally:
    if conn:
        conn.close()
