import psycopg2
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.tsa.holtwinters import ExponentialSmoothing

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

# Подключение к БД
conn = psycopg2.connect(
    host="localhost",
    database="gagarin",
    user="postgres",
    password="1"
)

# Получение данных
query = """
SELECT flight_date, departure_time, airport, aircraft_type
FROM flights
WHERE flight_date < '2025-04-01'
"""

df = pd.read_sql(query, conn)
conn.close()

# Обработка дат
df['flight_date'] = pd.to_datetime(df['flight_date'])
df['departure_time'] = pd.to_datetime(df['departure_time'], format='%H:%M').dt.hour

# Подсчёт общего числа дней
total_days = (df['flight_date'].max() - df['flight_date'].min()).days + 1

# Подсчёт количества рейсов по дням
daily_counts = df.groupby('flight_date').size()

# Прогноз с использованием Exponential Smoothing
model = ExponentialSmoothing(daily_counts, trend='add', seasonal='add', seasonal_periods=7)
fit = model.fit()
future_dates = pd.date_range(start='2025-04-01', end='2025-08-31')
forecast = fit.forecast(len(future_dates))
forecast = pd.Series(forecast.values, index=future_dates)

# Обрезаем прогноз на период с 1 мая по 31 августа
forecast_period = pd.date_range(start='2025-05-01', end='2025-08-31')
forecast_subset = forecast.loc[forecast_period]

# Построение столбчатой диаграммы прогноза
plt.figure(figsize=(16,6))
plt.bar(forecast_subset.index, forecast_subset.values, color='mediumseagreen')
plt.title('Прогноз количества рейсов по дням (май – август 2025)', fontsize=14)
plt.xlabel('Дата')
plt.ylabel('Количество рейсов')
plt.grid(True, axis='y')
plt.xticks(
    pd.date_range(start='2025-05-01', end='2025-08-31', freq='7D'),
    [d.strftime('%d-%m') for d in pd.date_range(start='2025-05-01', end='2025-08-31', freq='7D')],
    rotation=45
)
plt.tight_layout()
plt.savefig('prognoz_bar_po_dnyam_mai_avgust.png')
