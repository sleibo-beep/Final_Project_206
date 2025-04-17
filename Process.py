import sqlite3

DB_NAME = "final_project.db"
DATE = "2025-04-15"
OUTPUT_FILE = "overall_avg_aqi.txt"

def calculate_overall_aqi():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute('''
        SELECT ROUND(AVG(aqi), 2) 
        FROM AirQualityData
        WHERE date = ?
    ''', (DATE,))
    
    result = cur.fetchone()[0]
    conn.close()

    with open(OUTPUT_FILE, "w") as f:
        f.write(f"Average AQI across all ZIP codes and pollutants on {DATE}: {result}\n")


if __name__ == "__main__":
    calculate_overall_aqi()