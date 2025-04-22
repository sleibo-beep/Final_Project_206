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
                WeatherData.temp,
                WeatherData.pressure,
                WeatherData.humidity,
                AirQualityData.pollutant_id,
                AirQualityData.aqi
            FROM WeatherData
            JOIN AirQualityData
                ON WeatherData.zip = AirQualityData.zip
            LIMIT 25
        '''
        df = pd.read_sql_query(query, conn)
        if df.empty:
            print("\nJoin ran but returned no results.")
        else:
            print("\nJoin result:")
            print(df)

            df.to_sql('WeatherAirQualityJoin', conn, if_exists='replace', index=False)
            print("\nJoin result inserted into table 'WeatherAirQualityJoin'")
    except Exception as e:
        print("\nError running join query:", e)
    conn.close()


def main():
    print_sample_tables()
    run_join_query()

if __name__ == "__main__":
    main()