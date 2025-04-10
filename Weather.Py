import requests
import sqlite3
import time
from datetime import datetime

# --- CONFIGURATION ---
# API_KEY = "f86bdf89ba9b235fa5ed7e263b6808bd"
# BASE_URL = "http://history.openweathermap.org/data/2.5/history/city"
DB_NAME = "final_project.db"

# Sample city list: you can add more (OpenWeatherMap city IDs)
CITIES = [
    {"id": 5128581, "name": "New York", "zip":10023},
    {"id": 5391959, "name": "San Francisco","zip":48103},
    {"id": 4887398, "name": "Chicago","zip": 22203},
    {"id": 2643743, "name": "London","zip":44004},
    {"id": 2968815, "name": "Paris","zip":90210},
]

def get_weather(zip):
  open_api_key = "f86bdf89ba9b235fa5ed7e263b6808bd"
  base = "https://api.openweathermap.org/data/2.5/weather"
  param1 = f"appid={open_api_key}"
  param2 = f"zip={zip}"
  param3 = f"units=Imperial"
  request = f"{base}?{param1}&{param2}&{param3}"

  # print(request)
  page = requests.get(request)
  # print(page.status_code) #to check if the request is successful
  weather  = page.json()    #turn the information into a json object
  return weather

#Show this first test1 as an example, point out the temperature may will be different



# --- DATABASE SETUP ---
def create_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS WeatherData (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER,
            city_name TEXT,
            date TEXT,
            rainfall REAL,
            snowfall REAL,
            wind_gust REAL,
            UNIQUE(city_id, date)
        )
    ''')
    conn.commit()
    conn.close()

# --- FETCH AND STORE ---
def fetch_weather(city_id, city_name):
    params = {
        "id": city_id,
        "type": "hour",
        "appid": API_KEY,
        "units": "metric"
    }
    response = requests.get(BASE_URL, params=params)
    if response.status_code != 200:
        print(f"Failed to fetch data for {city_name}")
        return []

    data = response.json()
    weather_list = data.get("list", [])[:25]  # Only take first 25 entries

    records = []
    for entry in weather_list:
        dt = datetime.utcfromtimestamp(entry["dt"]).strftime('%Y-%m-%d')
        rain = entry.get("rain", {}).get("1h", 0)
        snow = entry.get("snow", {}).get("1h", 0)
        gust = entry.get("wind", {}).get("gust", 0)
        records.append((city_id, city_name, dt, rain, snow, gust))

    return records

# --- INSERT INTO DB ---
def insert_weather_data(records):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for record in records:
        cur.execute('''
            INSERT OR IGNORE INTO WeatherData (city_id, city_name, date, rainfall, snowfall, wind_gust)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', record)
    conn.commit()
    conn.close()

# --- MAIN FUNCTION ---
def main():
    import json
    # test1 = get_weather(48103)
    # print(json.dumps(test1, indent = 2))

    create_db()
    for city in CITIES:
        print(city)
        data = get_weather(city["zip"])
        print(json.dumps(data, indent = 2))
        # records = fetch_weather(city["id"], city["name"])
        # insert_weather_data(records)
        # print(f"Inserted {len(records)} weather entries for {city['name']}")

if __name__ == "__main__":
    main()