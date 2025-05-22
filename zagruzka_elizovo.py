import psycopg2
import json

def create_connection():
    return psycopg2.connect(
        host="localhost",
        database="gagarin",
        user="postgres",
        password="1"
    )

def create_elizovo_table(conn):
    with conn.cursor() as cursor:
        cursor.execute('''
        DROP TABLE IF EXISTS elizovo_flights;

        CREATE TABLE elizovo_flights (
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
        print("Таблица elizovo_flights успешно создана!")

def load_elizovo_data(conn, json_file):
    with open(json_file, 'r', encoding='utf-8') as f:
        data = json.load(f)

    with conn.cursor() as cursor:
        for flight in data:
            try:
                cursor.execute('''
                INSERT INTO elizovo_flights (
                    schedule_date, departure_time, arrival_time,
                    days_of_week, period, airline,
                    flight_number, aircraft_type, airport
                ) VALUES (
                    %(date)s, %(departure)s, %(arrival)s,
                    %(days)s::jsonb, %(period)s, %(airline)s,
                    %(flight_number)s, %(aircraft_type)s, %(airport)s
                )
                ''', {
                    'date': flight.get('Дата расписания', ''),
                    'departure': flight.get('Отправление', ''),
                    'arrival': flight.get('Прибытие', ''),
                    'days': json.dumps(flight.get('Дни полетов', []), ensure_ascii=False),
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
    print(f"Загружено {len(data)} записей в таблицу elizovo_flights.")

# Основной запуск
try:
    conn = create_connection()
    create_elizovo_table(conn)
    load_elizovo_data(conn, "C:/Users/Alina/Desktop/pytonchek/Elizovo.json")
except Exception as e:
    print(f"Произошла ошибка: {e}")
finally:
    if conn:
        conn.close()
