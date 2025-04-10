# hey rachel!

import requests
import sqlite3

# --- CONFIG ---
API_KEY = "3a6fe0a979d0cce6c60ca539"
BASE_URL = "https://v6.exchangerate-api.com/v6/3a6fe0a979d0cce6c60ca539/latest/USD"
DB_NAME = "hotel_data.db"

# --- STEP 1: Fetch data from API ---
def get_hotel_price(checkin, checkout):
    url = f"{BASE_URL}?hotelid=1450057&currency=USD&rooms=1&adults=2&checkin={checkin}&checkout={checkout}&api_key={API_KEY}"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        try:
            price = float(data["expedia"][0]["price"])
            return price
        except Exception as e:
            print("Error extracting price:", e)
    else:
        print("API call failed with status code", response.status_code)
    
    return None

# --- STEP 2: Set up SQLite database ---
def create_table():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        CREATE TABLE IF NOT EXISTS HotelPrices (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            checkin TEXT,
            checkout TEXT,
            price REAL
        )
    ''')
    conn.commit()
    conn.close()

# --- STEP 3: Insert into database ---
def insert_price(checkin, checkout, price):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute('''
        INSERT INTO HotelPrices (checkin, checkout, price)
        VALUES (?, ?, ?)
    ''', (checkin, checkout, price))
    conn.commit()
    conn.close()
    print(f"✅ Inserted: {checkin} to {checkout} for ${price}")

# --- MAIN WORKFLOW ---
def main():
    create_table()
    checkin = "2025-12-10"
    checkout = "2025-12-11"
    
    price = get_hotel_price(checkin, checkout)
    if price:
        insert_price(checkin, checkout, price)

if __name__ == "__main__":
    main()