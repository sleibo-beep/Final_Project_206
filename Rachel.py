# hey rachel!

# hotel_data.py
# Fetches hotel data and stores it in a separate SQLite DB

import requests
import sqlite3
from datetime import datetime, timedelta
import json

HOTEL_API_KEY = "67ebff1af65898f678660136"
DB_NAME = "hotel.db"

conn = sqlite3.connect(DB_NAME)
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS HotelPrices (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        hotel_id TEXT,
        location TEXT,
        checkin TEXT,
        checkout TEXT,
        price REAL,
        UNIQUE(hotel_id, checkin, checkout)
    )
''')
conn.commit()


def fetch_hotel_price(hotel_id: str, checkin: str, checkout: str):
    url = f"https://api.makcorps.com/expedia?hotelid={hotel_id}&currency=USD&rooms=1&adults=2&checkin={checkin}&checkout={checkout}&api_key={HOTEL_API_KEY}"
    try:
        resp = requests.get(url)
        data = resp.json()

        if "data" not in data or not data["data"]:
            print(f"[NO DATA] hotel_id={hotel_id}, checkin={checkin}, checkout={checkout}")
            print(json.dumps(data, indent=2))
            return None

        price = float(data['data'][0]['price'])
        return price
    except Exception as e:
        print(f"[ERROR] hotel_id={hotel_id}, checkin={checkin}: {e}")
        return None


def insert_hotel_data(hotel_id: str, location: str, start_date: str, days: int):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    count = 0
    for i in range(days):
        if count >= 25:
            break
        checkin = (start + timedelta(days=i)).strftime("%Y-%m-%d")
        checkout = (start + timedelta(days=i + 1)).strftime("%Y-%m-%d")
        if cursor.execute("SELECT 1 FROM HotelPrices WHERE hotel_id=? AND checkin=? AND checkout=?", (hotel_id, checkin, checkout)).fetchone():
            continue
        price = fetch_hotel_price(hotel_id, checkin, checkout)
        if price:
            cursor.execute("""
                INSERT OR IGNORE INTO HotelPrices (hotel_id, location, checkin, checkout, price)
                VALUES (?, ?, ?, ?, ?)
            """, (hotel_id, location, checkin, checkout, price))
            conn.commit()
            count += 1


if __name__ == "__main__":
    insert_hotel_data("1450057", "Ann Arbor", "2024-12-01", 40)
    conn.close()
