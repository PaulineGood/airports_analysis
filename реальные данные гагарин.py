import requests
from bs4 import BeautifulSoup
import pandas as pd
import json

url = "https://ar-gsv.ru/schedule/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
}

response = requests.get(url, headers=headers)
soup = BeautifulSoup(response.text, "html.parser")

table = soup.find("table")
rows = table.find_all("tr")

data = []
current_direction = None

for row in rows:
    cols = row.find_all("td")

    # Город — один <td> с colspan=8
    if len(cols) == 1 and cols[0].get("colspan") == "8":
        current_direction = cols[0].get_text(strip=True)
        continue

    if len(cols) == 8:
        dep_time = cols[0].get_text(strip=True)
        arr_time = cols[1].get_text(strip=True)
        days = cols[2].get_text(strip=True)
        period = cols[3].get_text(strip=True)
        airline = cols[4].find("div", class_="table-aircompany-logo-alt")
        airline = airline.get_text(strip=True) if airline else "N/A"
        flight = cols[5].get_text(strip=True)
        aircraft = cols[6].get_text(strip=True)
        airport = cols[7].get_text(strip=True)

        data.append({
            "Направление": current_direction,
            "Отправление": dep_time,
            "Прибытие": arr_time,
            "Дни полетов": days,
            "Период": period,
            "Авиакомпания": airline,
            "№ Рейса": flight,
            "Тип судна": aircraft,
            "Аэропорт": airport
        })

# Сохраняем в JSON
with open("schedule.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ Сохранено {len(data)} записей в schedule.json")
