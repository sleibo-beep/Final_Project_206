import requests
import sqlite3

api_key = "d3e23e370dffc1de116d4a28d2e71c41"
api_url = "http://api.weatherstack.com/historical"
db_name = "final_project.db"
dates = [
    ("2025-12-01", "2025-12-02"),
    ("2025-12-03", "2025-12-04"),
    ("2025-12-05", "2025-12-06"),
    ("2025-12-07", "2025-12-08"),
    ("2025-12-09", "2025-12-10")
]
response = requests.get(api_url)

def get_weather_data(date, location="New York"):
    params = {
        "access_key": api_key,
        "query": location,
        "historical_date": date,
        "hourly": "1"
    }
    response = requests.get(api_url, params=params)
    if response.status_code == 200:
        data = response.json()
    return None

def weather_exists(date):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('SELECT id FROM WeatherData WHERE date = ?', (date,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def insert_weather_data(date, rainfall, snowfall, wind_gust):
    conn = sqlite3.connect(db_name)
    cur = conn.cursor()
    cur.execute('''
        INSERT OR IGNORE INTO WeatherData (date, rainfall, snowfall, wind_gust)
        VALUES (?, ?, ?, ?)
    ''', (date, rainfall, snowfall, wind_gust))
    conn.commit()
    conn.close()