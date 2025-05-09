import requests
import sqlite3
import random

API_KEY = "B7D7AAE3-FBF1-4349-990F-9302D082B292"
BASE_URL = "https://www.airnowapi.org/aq/forecast/zipCode/"
DB_NAME = "final_project.db"

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


def create_tables():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''
        CREATE TABLE IF NOT EXISTS AirQualityData (
            zip INTEGER PRIMARY KEY,
            aqi INTEGER,
            pollutant_id INTEGER,
            FOREIGN KEY (pollutant_id) REFERENCES Pollutants(id)
        )
    ''')

    cur.execute('''
        CREATE TABLE IF NOT EXISTS Pollutants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE
        )
    ''')

    conn.commit()
    conn.close()

def fetch_air_quality(zip_code):
    params = {
        "format": "application/json",
        "zipCode": zip_code,
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

        if pollutant and aqi is not None:
            records.append((zip_code, aqi, pollutant))

    return records

def insert_air_quality(records):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    for zip_code, aqi, pollutant in records:
        if aqi == -1:
            continue  

        cur.execute("SELECT 1 FROM AirQualityData WHERE zip = ?", (zip_code,))
        if cur.fetchone():
            continue

        cur.execute("SELECT id FROM Pollutants WHERE name = ?", (pollutant,))
        result = cur.fetchone()

        if result:
            pollutant_id = result[0]
        else:
            cur.execute("SELECT MAX(id) FROM Pollutants")
            max_id = cur.fetchone()[0] or 0
            new_id = max_id + 1

            cur.execute("INSERT INTO Pollutants (id, name) VALUES (?, ?)", (new_id, pollutant))
            pollutant_id = new_id

        cur.execute('''
            INSERT INTO AirQualityData (zip, aqi, pollutant_id)
            VALUES (?, ?, ?)
        ''', (zip_code, aqi, pollutant_id))

    conn.commit()
    conn.close()

def main():
    create_tables()

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT zip FROM AirQualityData")
    stored_zips = set(row[0] for row in cur.fetchall())
    conn.close()

    remaining_zips = [z for z in ZIP_CODES if z not in stored_zips]
    random.shuffle(remaining_zips)
    chunk = remaining_zips[:25]

    if not chunk:
        print("All zip codes have already been fetched.")
        return

    print(f"\nFetching AQI data for {len(chunk)} new zip codes...\n")
    for zip_code in chunk:
        records = fetch_air_quality(zip_code)
        if records:
            insert_air_quality(records)

    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) FROM AirQualityData")
    total_rows = cur.fetchone()[0]
    print(f"\nTotal rows in AQI: {total_rows}")
    conn.close()


if __name__ == "__main__":
    main()