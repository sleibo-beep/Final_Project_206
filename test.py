import requests
import sqlite3
from datetime import datetime

# --- CONFIGURATION ---
API_KEY = "199F9B5F-EC89-4A51-BB86-F2303C738B15"
BASE_URL = "https://www.airnowapi.org/aq/forecast/zipCode/"
DB_NAME = "final_project.db"
DATE = "2025-04-15"  # You can also use datetime.now().strftime('%Y-%m-%d')

ZIP_CODES = [
    "10001", "94103", "60601", "77001", "85001", "19104", "30303", "98101", "48201", "02201",
    "33101", "80202", "55401", "64106", "46204", "73102", "96813", "20001", "37201", "21201"
]  # use 20-25 at a time for safe API use

# --- 1. Create the table ---
def create_airquality_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS AirQualityData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zip TEXT,
            date TEXT,
            pollutant TEXT,
            aqi INTEGER,
            category TEXT,
            UNIQUE(zip, date, pollutant)
        )
    ''')
    conn.commit()
    conn.close()

# --- 2. Fetch data from AirNow API ---
def fetch_air_quality(zip_code):
    params = {
        "format": "application/json",
        "zipCode": zip_code,
        "date": DATE,
        "distance": 25,
        "API_KEY": API_KEY
    }

    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Failed for {zip_code} — {response.status_code}")
        return []

    try:
        results = response.json()
    except:
        print(f"Failed to parse JSON for {zip_code}")
        return []

    records = []
    for item in results:
        pollutant = item.get("ParameterName")
        aqi = item.get("AQI")
        category = item.get("Category", {}).get("Name")
        date = item.get("DateForecast")

        if pollutant and aqi is not None:
            records.append((zip_code, date, pollutant, aqi, category))

    return records

# --- 3. Insert into database ---
def insert_air_quality(records):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for record in records:
        cur.execute('''
            INSERT OR IGNORE INTO AirQualityData (zip, date, pollutant, aqi, category)
            VALUES (?, ?, ?, ?, ?)
        ''', record)
    conn.commit()
    conn.close()

# --- 4. Main driver function ---
def main():
    create_airquality_table()
    for zip_code in ZIP_CODES:
        print(f" Fetching AQI for {zip_code}")
        records = fetch_air_quality(zip_code)
        insert_air_quality(records)
    print("Air quality data inserted.")

if __name__ == "__main__":
    main()