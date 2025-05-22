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
        DROP TABLE IF EXISTS flights;
        
        CREATE TABLE flights (
            id SERIAL PRIMARY KEY,
            schedule_date TEXT,
            departure_time TEXT,
            arrival_time TEXT,
            days_of_week JSONB,
            period TEXT,
            airline TEXT,
            flight_number TEXT,
            aircraft_type TEXT,
            airport TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        conn.commit()
        print("Таблица успешно создана!")

def load_data(conn, json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with conn.cursor() as cursor:
        for flight in data:
            # Обработка всех возможных вариантов данных
            try:
                cursor.execute('''
                INSERT INTO flights (
                    schedule_date, departure_time, arrival_time,
                    days_of_week, period, airline,
                    flight_number, aircraft_type, airport
                ) VALUES (
                    %(date)s, %(departure)s, %(arrival)s,
                    %(days)s::jsonb, %(period)s, %(airline)s,
                    %(flight_number)s, %(aircraft_type)s, %(airport)s
                )
                ''', {
                    'date': flight.get('Дата расписания', 'N/A'),
                    'departure': flight.get('Отправление', ''),
                    'arrival': flight.get('Прибытие', ''),
                    'days': json.dumps(flight.get('Дни полетов', [])),
                    'period': flight.get('Период', ''),
                    'airline': flight.get('Авиакомпания', ''),
                    'flight_number': flight.get('Номер рейса', ''),
                    'aircraft_type': flight.get('Тип судна', ''),
                    'airport': flight.get('Аэропорт', '')
                })
            except Exception as e:
                print(f"Ошибка при вставке записи: {flight}")
                print(f"Текст ошибки: {e}")
        
        conn.commit()
        print(f"Успешно загружено {len(data)} записей!")

# Основной процесс
try:
    conn = create_connection()
    create_table(conn)
    load_data(conn, "C:/Users/Alina/Desktop/all_flights.json")  # Укажите путь к вашему файлу
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    if conn:
        conn.close()