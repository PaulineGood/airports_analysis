import psycopg2
import json

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
            direction TEXT,
            departure_time TEXT,
            arrival_time TEXT,
            days_of_week JSONB,
            period TEXT,
            airline TEXT,
            flight_number TEXT,
            aircraft_type TEXT,
            airport TEXT,
            flight_date DATE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        ''')
        conn.commit()
        print("Таблица успешно создана!")

def parse_days(days):
    if not days:
        return []
    if isinstance(days, list):
        return days
    if isinstance(days, str):
        return [d.strip() for d in days.split(",")]
    return []


def load_data(conn, json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    with conn.cursor() as cursor:
        for flight in data:
            try:
                cursor.execute('''
                INSERT INTO flights (
                    direction, departure_time, arrival_time,
                    days_of_week, period, airline,
                    flight_number, aircraft_type, airport, flight_date
                ) VALUES (
                    %(direction)s, %(departure)s, %(arrival)s,
                    %(days)s::jsonb, %(period)s, %(airline)s,
                    %(flight_number)s, %(aircraft_type)s, %(airport)s, %(flight_date)s
                )
                ''', {
                    'direction': flight.get('Направление', ''),
                    'departure': flight.get('Отправление', ''),
                    'arrival': flight.get('Прибытие', ''),
                    'days': json.dumps(parse_days(flight.get('Дни полетов', ''))),
                    'period': flight.get('Период', ''),
                    'airline': flight.get('Авиакомпания', ''),
                    'flight_number': flight.get('№ Рейса', ''),
                    'aircraft_type': flight.get('Тип судна', ''),
                    'airport': flight.get('Аэропорт', ''),
                    'flight_date': flight.get('Дата рейса', None)
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
    load_data(conn, "C:/Users/Alina/Desktop/pytonchek/all_flights_by_date.json")  # путь к твоему файлу
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    if conn:
        conn.close()
