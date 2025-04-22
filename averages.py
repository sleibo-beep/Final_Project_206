import sqlite3
import matplotlib as plt

# Connect to the database
conn = sqlite3.connect("final_project.db")
cursor = conn.cursor()

# SQL query: Join all 3 tables to get pollutant name, AQI, and temperature
query = '''
    SELECT 
        Pollutants.name AS pollutant,
        AirQualityData.aqi,
        WeatherData.temp
    FROM AirQualityData
    JOIN Pollutants ON AirQualityData.pollutant_id = Pollutants.id
    JOIN WeatherData ON AirQualityData.zip = WeatherData.zip
'''

results = cursor.execute(query).fetchall()
conn.close()

# Aggregate values per pollutant
pollutant_data = {}
for pollutant, aqi, temp in results:
    if pollutant not in pollutant_data:
        pollutant_data[pollutant] = {'aqi_total': 0, 'temp_total': 0, 'count': 0}
    pollutant_data[pollutant]['aqi_total'] += aqi
    pollutant_data[pollutant]['temp_total'] += temp
    pollutant_data[pollutant]['count'] += 1

# Write the output to a text file
with open("final_project_averages.txt", "w") as f:
    f.write("Average AQI and Temperature by Pollutant\n")
    for pollutant, data in pollutant_data.items():
        avg_aqi = data['aqi_total'] / data['count']
        avg_temp = data['temp_total'] / data['count']
        f.write(f"Pollutant: {pollutant}\n")
        f.write(f"  Average AQI: {avg_aqi:.2f}\n")
        f.write(f"  Average Temperature: {avg_temp:.2f} °F\n\n")


