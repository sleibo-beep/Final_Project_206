import sqlite3
import pandas as pd

DB_NAME = "final_project.db"

def print_sample_tables():
    conn = sqlite3.connect(DB_NAME)
    print("\nWeatherData sample:")
    try:
        df_weather = pd.read_sql_query("SELECT * FROM WeatherData LIMIT 5;", conn)
        print(df_weather)
    except Exception as e:
        print("Error reading WeatherData:", e)

    print("\nAirQualityData sample:")
    try:
        df_air = pd.read_sql_query("SELECT * FROM AirQualityData LIMIT 5;", conn)
        print(df_air)
    except Exception as e:
        print("Error reading AirQualityData:", e)
    conn.close()

def run_join_query():
    conn = sqlite3.connect(DB_NAME)
    try:
        query = '''
            SELECT 
                WeatherData.zip,
                substr(WeatherData.date, 1, 10) AS date,
                WeatherData.temp,
                WeatherData.pressure,
                WeatherData.humidity,
                AirQualityData.pollutant,
                AirQualityData.aqi,
                AirQualityData.category
            FROM WeatherData
            JOIN AirQualityData
                ON WeatherData.zip = AirQualityData.zip
                AND substr(WeatherData.date, 1, 10) = AirQualityData.date
            ORDER BY date DESC
            LIMIT 10
        '''
        df = pd.read_sql_query(query, conn)
        if df.empty:
            print("\nJoin ran but returned no results.")
        else:
            print("\nJoin result:")
            print(df)
    except Exception as e:
        print("\nError running join query:", e)
    conn.close()

def main():
    print_sample_tables()
    run_join_query()

if __name__ == "__main__":
    main()