import requests
import sqlite3
from datetime import datetime
import random

# --- CONFIGURATION ---
API_KEY = "BF559927-DC09-44A6-B56C-2D51E5751C9D"
BASE_URL = "https://www.airnowapi.org/aq/forecast/zipCode/"
DB_NAME = "final_project.db"
DATE = "2025-04-15"  # You can also use datetime.now().strftime('%Y-%m-%d')

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
# --- 1. Create the table ---
def create_airquality_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS AirQualityData (
            zip INTEGER PRIMARY KEY ,
            date TEXT,
            pollutant TEXT,
            aqi INTEGER,
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
        date = item.get("DateForecast")
        #print(item)

        if pollutant and aqi is not None:
            records.append((zip_code, date, pollutant, aqi))
        

    return records

# --- 3. Insert into database ---
def insert_air_quality(records):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for record in records:
        cur.execute('''
            INSERT OR IGNORE INTO AirQualityData (zip, date, pollutant, aqi)
            VALUES (?, ?, ?, ?)
        ''', record)
    conn.commit()
    conn.close()

# --- 4. Main driver function ---
def main():
    create_airquality_table()
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Get zip codes already in DB
    cur.execute("SELECT DISTINCT zip FROM AirQualityData")
    stored_zips = set(row[0] for row in cur.fetchall())

    # Filter out zips that are already in DB
    remaining_zips = [z for z in ZIP_CODES if z not in stored_zips]
    random.shuffle(remaining_zips)

    chunk = remaining_zips[:25]  # Take the next 25 new ones

    if not chunk:
        print("All zip codes have already been fetched.")
        conn.close()
        return

    print(f"\n\n\nFetching AQI data for {len(chunk)} new zip codes...\n")
    for zip_code in chunk:
        records = fetch_air_quality(zip_code)
        if records:
            insert_air_quality(records)

    # Optional: Print updated total
    cur.execute("SELECT COUNT(*) FROM AirQualityData")
    total_rows = cur.fetchone()[0]
    print(f"\nTotal rows in AQI: {total_rows}")

    conn.close()
if __name__ == "__main__":
    main()