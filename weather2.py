import requests
import sqlite3
from datetime import datetime

DB_NAME = "final_project.db"

CITIES = [
    {"id": 5128581, "name": "New York", "zip": 10023},
    {"id": 5391959, "name": "San Francisco", "zip": 94103},
    {"id": 4887398, "name": "Chicago", "zip": 60601},
    {"id": 2643743, "name": "London", "zip": "SW1A 1AA,GB"},  # add country for non-US
    {"id": 2968815, "name": "Paris", "zip": "75001,FR"},
]

API_KEY = "f86bdf89ba9b235fa5ed7e263b6808bd"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS WeatherData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER,
            city_name TEXT,
            date TEXT,
            temp FLOAT,
            pressure INTEGER,
            humidity INTEGER,
            UNIQUE(city_id, date)
        )
    ''')
    conn.commit()
    conn.close()

def fetch_and_clean(zip_code, city_id, city_name):
    params = {
        "appid": API_KEY,
        "zip": zip_code,
        "units": "imperial"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch data for {city_name}, status code {response.status_code}")
        return []

    data = response.json()
    temp = data.get("main", {}).get("temp", 0)
    pressure = data.get("main", {}).get("pressure", 0)
    humidity = data.get("main", {}).get("humidity", 0)
    date = datetime.utcnow().strftime('%Y-%m-%d')

    return [(city_id, city_name, date, temp, pressure, humidity)]

def insert_weather_data(records):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for record in records:
        print("Inserting:", record)
        cur.execute('''
            INSERT OR IGNORE INTO WeatherData (city_id, city_name, date, temp, pressure, humidity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', record)
    conn.commit()
    conn.close()

def main():
    create_db()

    for city in CITIES:
        records = fetch_and_clean(city["zip"], city["id"], city["name"])
        if records:
            insert_weather_data(records)

if __name__ == "__main__":
    main()