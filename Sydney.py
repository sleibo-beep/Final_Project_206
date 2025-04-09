WEATHER_API_KEY = "d3e23e370dffc1de116d4a28d2e71c41"
WEATHER_BASE_URL = "http://api.weatherstack.com/historical"
DB_NAME = "final_project.db"
DATES = [
    ("2025-12-01", "2025-12-02"),
    ("2025-12-03", "2025-12-04"),
    ("2025-12-05", "2025-12-06"),
    ("2025-12-07", "2025-12-08"),
    ("2025-12-09", "2025-12-10")
]

def get_weather_data(date, location="New York"):
    params = {
        "access_key": WEATHER_API_KEY,
        "query": location,
        "historical_date": date,
        "hourly": "1"
    }
    response = requests.get(WEATHER_BASE_URL, params=params)
    if response.status_code == 200:
        return response.json()
    return None

def weather_exists(date):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('SELECT id FROM WeatherData WHERE date = ?', (date,))
    result = cur.fetchone()
    conn.close()
    return result is not None

def insert_weather_data(date, rainfall, snowfall, wind_gust):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        INSERT OR IGNORE INTO WeatherData (date, rainfall, snowfall, wind_gust)
        VALUES (?, ?, ?, ?)
    ''', (date, rainfall, snowfall, wind_gust))
    conn.commit()
    conn.close()