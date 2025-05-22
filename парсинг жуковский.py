import requests
from bs4 import BeautifulSoup
import json

URL = "https://web.archive.org/web/20170301094702/http://www.zia.aero/index.php?id="

response = requests.get(URL)
soup = BeautifulSoup(response.content, "lxml")

flights_data = []

lines = soup.select("div#scrollable div.line")
for line in lines:
    flight = {}
    flight["flight_number"] = line.get("city", "").strip()
    flight["destination"] = line.get("napr", "").strip()
    flight["airline"] = line.get("airlane", "").strip()
    flight["date"] = line.get("date", "").strip()
    flight["time"] = line.get("time", "").strip()

    # Альтернативно извлекаем визуальные поля
    time_text = line.select_one(".col-time")
    flight["time_text"] = time_text.text.strip() if time_text else ""

    status_p = line.select_one(".col-status p")
    flight["status"] = status_p.text.strip() if status_p else ""

    flights_data.append(flight)

# Сохраняем в JSON
with open("zhukovsky_flights.json", "w", encoding="utf-8") as f:
    json.dump(flights_data, f, ensure_ascii=False, indent=2)

print(f"Извлечено {len(flights_data)} рейсов.")
