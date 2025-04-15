import requests
import sqlite3
import time
import random
from datetime import datetime

# --- CONFIGURATION ---
DB_NAME = "final_project.db"
API_KEY = "f86bdf89ba9b235fa5ed7e263b6808bd"
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"

# --- ZIP CODE LIST ---
ZIP_CODES = [
    "10001", "94103", "60601", "77001", "85001", "19104", "30303", "98101", "48201", "02201",
    "33101", "80202", "55401", "64106", "46204", "73102", "96813", "20001", "37201", "21201",
    "14201", "27601", "29201", "32801", "37203", "53202", "53211", "10019", "10023", "10003",
    "30309", "60611", "70112", "75201", "28202", "85301", "48226", "10036", "10024", "94114",
    "95814", "97209", "63103", "64108", "73103", "85004", "55403", "19103", "19106", "20005"
    # Add more if needed – at least 100 for real project
]

# --- DATABASE SETUP ---
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS WeatherData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zip TEXT,
            date TEXT,
            temp FLOAT,
            pressure INTEGER,
            humidity INTEGER,
            UNIQUE(zip, date)
        )
    ''')
    conn.commit()
    conn.close()

# --- FETCH WEATHER FOR A SINGLE ZIP ---
def fetch_and_clean(zip_code, city_id=None, city_name=None):
    params = {
        "appid": API_KEY,
        "zip": zip_code,
        "units": "imperial"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch data for {zip_code} – Status: {response.status_code}")
        return []

    data = response.json()

    temp = data.get("main", {}).get("temp", 0)
    pressure = data.get("main", {}).get("pressure", 0)
    humidity = data.get("main", {}).get("humidity", 0)
    date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    city_name = city_name or f"ZIP_{zip_code}"

    return [(city_id, city_name, date, temp, pressure, humidity)]

# --- INSERT WEATHER INTO DB ---
def insert_weather_data(records):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for record in records:
        cur.execute('''
            INSERT OR IGNORE INTO WeatherData (city_id, city_name, date, temp, pressure, humidity)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', record)
    conn.commit()
    conn.close()

# --- MAIN DRIVER FUNCTION ---
def main():
    create_db()

    all_zips = ZIP_CODES.copy()
    random.shuffle(all_zips)

    chunk_size = 25
    chunks = [all_zips[i:i + chunk_size] for i in range(0, len(all_zips), chunk_size)]

    for i, zip_chunk in enumerate(chunks):
        print(f"\n API Run {i + 1}/{len(chunks)} — Fetching data for {len(zip_chunk)} zip codes")
        for zip_code in zip_chunk:
            records = fetch_and_clean(zip_code)
            if records:
                insert_weather_data(records)
      

    # Optional: Check total rows
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM WeatherData")
    total_rows = cur.fetchone()[0]
    print(f"\n All done! Total rows in WeatherData table: {total_rows}")
    conn.close()

if __name__ == "__main__":
    main()