import requests
import sqlite3

# --- CONFIG ---
DB_NAME = "final_project.db"
ZIP_API_KEY = "b83257a0-1624-11f0-8d23-dfd3fb3c5a70"
ZIP_API_BASE = "https://app.zipcodebase.com/api/v1/search"

# --- ZIP LIST (modify or expand this) ---
ZIP_LIST = [
    "10001", "10002", "10003", "10004", "10005",
    "90210", "30301", "60601", "94103", "33101",
    "15213", "02108", "20001", "19104", "98101",
    "77001", "37201", "85001", "46204", "55401",
    "64106", "27601", "63103", "32801", "96813"
]  # 25 zip codes for one API run

# --- 1. Create the ZipCodes table ---
def create_zipcode_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS ZipCodes (
            zip TEXT PRIMARY KEY,
            city TEXT,
            state TEXT,
            country TEXT
        )
    ''')
    conn.commit()
    conn.close()

# --- 2. Fetch ZIP code metadata from ZipCodeBase ---
def fetch_zipcode_data(zip_codes):
    headers = {"apikey": ZIP_API_KEY}
    codes_str = codes_str = ",".join(zip_codes)
    params = {"codes": codes_str}

    response = requests.get(ZIP_API_BASE, headers=headers, params=params)
    if response.status_code != 200:
        print(f"❌ ZIP API failed: {response.status_code}")
        return []

    data = response.json().get("results", {})
    records = []

    for zip_code, results in data.items():
        if results:
            item = results[0]
            city = item.get("city", "Unknown")
            state = item.get("state", "Unknown")
            country = item.get("country_code", "Unknown")
            records.append((zip_code, city, state, country))

    return records

# --- 3. Insert ZIP records into the database ---
def insert_zipcode_data(records):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    for record in records:
        cur.execute('''
            INSERT OR IGNORE INTO ZipCodes (zip, city, state, country)
            VALUES (?, ?, ?, ?)
        ''', record)
    conn.commit()
    conn.close()

# --- 4. Run everything ---
def main():
    create_zipcode_table()
    records = fetch_zipcode_data(ZIP_LIST)
    insert_zipcode_data(records)
    print(f"✅ Inserted {len(records)} zip codes into the database.")

if __name__ == "__main__":
    main()