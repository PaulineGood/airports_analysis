import json

def clean_days_and_save(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    for flight in data:
        # Преобразовать "Дни полетов": ["вс"] → "вс"
        days = flight.get("Дни полетов", [])
        if isinstance(days, list) and days:
            flight["Дни полетов"] = days[0]
        else:
            flight["Дни полетов"] = ""

        # Удалить поле "Период", если есть
        if "Прибытие" in flight:
            del flight["Прибытие"]

        # Удалить поле "Период", если есть
        if "Период" in flight:
            del flight["Период"]

    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

    print(f"Файл сохранён: {output_path}")

# Пример использования:
clean_days_and_save(
    "C:/Users/Alina/Desktop/pytonchek/minvody_flights.json",
    "C:/Users/Alina/Desktop/pytonchek/minvody_flights_ready.json"
)

