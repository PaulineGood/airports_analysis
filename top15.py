import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np

# Названия аэропортов по кодам
airport_names = {
    'VKO': 'Внуково', 'SGC': 'Сургут', 'SVO': 'Шереметьево', 'DME': 'Домодедово',
    'AYT': 'Анталия', 'AER': 'Сочи (Адлер)', 'SIP': 'Симферополь', 'LED': 'Пулково',
    'SVX': 'Кольцово (Екатеринбург)', 'KRR': 'Пашковский (Краснодар)', 'GOI': 'Даболим (Гоа, Индия)',
    'MRV': 'Минеральные Воды', 'ROV': 'Платов (Ростов-на-Дону)', 'KZN': 'Казань', 'AAQ': 'Анапа',
    'OVB': 'Толмачёво (Новосибирск)', 'UFA': 'Уфа', 'TJM': 'Рощино (Тюмень)', 'EVN': 'Звартноц (Ереван, Армения)',
    'PFO': 'Пафос (Кипр)', 'GYD': 'Гейдар Алиев (Баку, Азербайджан)', 'SKG': 'Македония (Салоники, Греция)',
    'FEG': 'Фергана (Узбекистан)', 'NUX': 'Новый Уренгой', 'NBE': 'Энфида (Тунис)', 'FRU': 'Манас (Бишкек, Кыргызстан)',
    'SSH': 'Шарм-эль-Шейх (Египет)', 'MCX': 'Уйташ (Махачкала)', 'DYU': 'Душанбе (Таджикистан)', 'KGD': 'Храброво (Калининград)',
    'LBD': 'Худжанд (Таджикистан)', 'KUF': 'Курумоч (Самара)', 'HRG': 'Хургада (Египет)', 'GRV': 'Грозный',
    'ZIA': 'Жуковский', 'GOJ': 'Нижний Новгород', 'KQT': 'Бохтар (Таджикистан)', 'TJU': 'Куляб (Таджикистан)',
    'OSS': 'Ош (Кыргызстан)'
}

def plot_top_15_directions():
    # Подключение к БД
    conn = psycopg2.connect(
        host="localhost",
        database="gagarin",
        user="postgres",
        password="1"
    )

    # Загрузка аэропортов и дат
    query = "SELECT airport, flight_date FROM flights"
    df = pd.read_sql(query, conn)
    conn.close()

    # Преобразуем даты
    df['flight_date'] = pd.to_datetime(df['flight_date'])

    # Общая информация
    total_flights = len(df)
    start_date = df['flight_date'].min().strftime('%d.%m.%Y')
    end_date = df['flight_date'].max().strftime('%d.%m.%Y')

    # Подсчёт топ-15 направлений
    top_counts = df['airport'].value_counts().head(15)
    top_counts.index = [airport_names.get(code, code) for code in top_counts.index]

    # Цвета
    cmap = cm.get_cmap('tab20', len(top_counts))
    colors = [cmap(i) for i in range(len(top_counts))]

    # Построение графика
    plt.figure(figsize=(14, 8))
    bars = plt.bar(top_counts.index, top_counts.values, color=colors)

    # Подписи над столбцами
    for bar in bars:
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width()/2, height + 1, str(int(height)),
                 ha='center', va='bottom', fontsize=9)

    # Заголовки и подписи
    plt.title(f'Топ-15 самых популярных направлений по количеству рейсов\n'
              f'({start_date} – {end_date}, всего рейсов: {total_flights})', fontsize=14, weight='bold')
    plt.xlabel('Аэропорт назначения', fontsize=12)
    plt.ylabel('Количество рейсов', fontsize=12)
    plt.xticks(rotation=45, ha='right')
    plt.grid(axis='y', linestyle='--', alpha=0.6)

    plt.tight_layout()
    plt.savefig('top15_directions_colored.png', bbox_inches='tight')
    print("График сохранён в файл 'top15_directions_colored.png'")

plot_top_15_directions()
