import requests
import sqlite3
from datetime import datetime, timedelta
import json

WEATHER_API_KEY = "d3e23e370dffc1de116d4a28d2e71c41"
DB_NAME = "weather.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS Weather (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        location TEXT,
        date TEXT,
        rainfall REAL,
        snowfall REAL,
        wind_gust REAL,
        UNIQUE(location, date)
    )
''')
conn.commit()


def fetch_weather(location: str, date: str):
    url = f"http://api.weatherstack.com/historical?access_key={WEATHER_API_KEY}&query={location}&historical_date={date}&hourly=1"
    try:
        resp = requests.get(url)
        data = resp.json()

        if "historical" not in data or date not in data["historical"]:
            print(f"[NO DATA] location={location}, date={date}")
            print(json.dumps(data, indent=2))
            return None

        weather = data['historical'][date]['hourly'][0]
        rainfall = float(weather.get('precip', 0))
        snowfall = float(weather.get('snowfall', 0))
        wind_gust = float(weather.get('wind_gust', 0))
        return rainfall, snowfall, wind_gust
    except Exception as e:
        print(f"[ERROR] location={location}, date={date}: {e}")
        return None


def insert_weather_data(location: str, start_date: str, days: int):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    count = 0
    for i in range(days):
        if count >= 25:
            break
        date = (start + timedelta(days=i)).strftime("%Y-%m-%d")
        if cursor.execute("SELECT 1 FROM Weather WHERE location=? AND date=?", (location, date)).fetchone():
            continue
        result = fetch_weather(location, date)
        if result:
            rainfall, snowfall, wind_gust = result
            cursor.execute("""
                INSERT OR IGNORE INTO Weather (location, date, rainfall, snowfall, wind_gust)
                VALUES (?, ?, ?, ?, ?)
            """, (location, date, rainfall, snowfall, wind_gust))
            conn.commit()
            count += 1


if __name__ == "__main__":
    insert_weather_data("Ann Arbor", "2024-12-01", 40)
    conn.close()
