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
    "95814", "97209", "63103", "64108", "73103", "85004", "55403", "19103", "19106", "20005",
    "11201", "11215", "11217", "90001", "90012", "90024", "90064", "90089", "60614", "60637",
    "30308", "30318", "75204", "75206", "33139", "33140", "10002", "10009", "10010", "10011",
    "98103", "98109", "98115", "98133", "60622", "60647", "94117", "94121", "94122", "94131",
    "19107", "19123", "19130", "19147", "94109", "94110", "94111", "94016", "94040", "94043",
    "78701", "78702", "78704", "78705", "78741", "33125", "33126", "33127", "33130", "33132",
    "97201", "97202", "97203", "97206", "97210", "97212", "97214", "97217", "97219", "97221"
]

# --- DATABASE SETUP ---
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS WeatherData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            zip INTEGER,
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
def fetch_and_clean(zip_code):
    params = {
        "appid": API_KEY,
        "zip": zip_code,
        "units": "imperial"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f" Failed to fetch data for {zip_code} – Status: {response.status_code}")
        return []

    data = response.json()

    temp = data.get("main", {}).get("temp", 0)
    pressure = data.get("main", {}).get("pressure", 0)
    humidity = data.get("main", {}).get("humidity", 0)
    date = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')

    return [(zip_code, date, temp, pressure, humidity)]

# --- INSERT WEATHER INTO DB ---
def insert_weather_data(records):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for record in records:
        cur.execute('''
            INSERT OR IGNORE INTO WeatherData (zip, date, temp, pressure, humidity)
            VALUES (?, ?, ?, ?, ?)
        ''', record)
    conn.commit()
    conn.close()

# --- MAIN DRIVER FUNCTION ---
def main():
    create_db()

    # Connect once here to reuse
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get zip codes already in DB
    cur.execute("SELECT DISTINCT zip FROM WeatherData")
    stored_zips = set(row[0] for row in cur.fetchall())

    # Filter out zips that are already in DB
    remaining_zips = [z for z in ZIP_CODES if z not in stored_zips]
    random.shuffle(remaining_zips)

    chunk = remaining_zips[:25]  # Take the next 25 new ones

    if not chunk:
        print("All zip codes have already been fetched.")
        conn.close()
        return

    print(f"\nFetching weather data for {len(chunk)} new zip codes...\n")
    for zip_code in chunk:
        records = fetch_and_clean(zip_code)
        if records:
            insert_weather_data(records)

    # Optional: Print updated total
    cur.execute("SELECT COUNT(*) FROM WeatherData")
    total_rows = cur.fetchone()[0]
    print(f"\nTotal rows in WeatherData: {total_rows}")

    conn.close()

if __name__ == "__main__":
    main()