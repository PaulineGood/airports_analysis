import json
import pandas as pd
import matplotlib.pyplot as plt

def plot_real_data(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    df = pd.DataFrame(data)

    if 'Дата рейса' not in df.columns:
        print("Ошибка: поле 'Дата рейса' не найдено в данных.")
        return

    df['Дата рейса'] = pd.to_datetime(df['Дата рейса'], errors='coerce')
    df = df.dropna(subset=['Дата рейса'])

    start_date = pd.to_datetime("2025-05-01")
    end_date = pd.to_datetime("2025-08-31")
    df = df[(df['Дата рейса'] >= start_date) & (df['Дата рейса'] <= end_date)]

    if df.empty:
        print("Нет данных за период с 1 мая по 31 августа.")
        return

    counts_by_day = df.groupby(df['Дата рейса'].dt.date).size()

    plt.figure(figsize=(12, 6))
    counts_by_day.plot(kind='bar', color='skyblue')
    plt.xlabel('Дата')
    plt.ylabel('Количество рейсов')
    plt.title('Количество рейсов по дням (реальные данные)')

    # Показываем подписи через равные промежутки (например, каждую 5-ю дату)
    xticks = range(0, len(counts_by_day), 5)
    xtick_labels = [str(date) if i in xticks else '' for i, date in enumerate(counts_by_day.index)]
    plt.xticks(ticks=range(len(counts_by_day)), labels=xtick_labels, rotation=45)

    plt.tight_layout()
    plt.grid(True)
    plt.savefig('real.png')
    print("График сохранён в файл 'real.png'")

plot_real_data('expanded_schedule.json')
