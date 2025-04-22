import sqlite3
import matplotlib as plt

conn = sqlite3.connect("final_project.db")
cursor = conn.cursor()

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

pollutant_data = {}
for pollutant, aqi, temp in results:
    if pollutant not in pollutant_data:
        pollutant_data[pollutant] = {'aqi_total': 0, 'temp_total': 0, 'count': 0}
    pollutant_data[pollutant]['aqi_total'] += aqi
    pollutant_data[pollutant]['temp_total'] += temp
    pollutant_data[pollutant]['count'] += 1


conn = sqlite3.connect('final_project.db')
cursor = conn.cursor()

cursor.execute("SELECT AVG(temp) FROM WeatherData")
average_temp = cursor.fetchone()[0]

print("Average Temp:", average_temp)

cursor.execute("SELECT AVG(pressure) FROM WeatherData")
average_pressure = cursor.fetchone()[0]

print("Average Pressure:", average_pressure)

cursor.execute("SELECT AVG(humidity) FROM WeatherData")
average_humidity = cursor.fetchone()[0]

print("Average Humidity:", average_humidity)

conn.close()


with open("final_project_averages.txt", "w") as f:
    f.write("Average AQI and Temperature by Pollutant\n")
    for pollutant, data in pollutant_data.items():
        avg_aqi = data['aqi_total'] / data['count']
        avg_temp = data['temp_total'] / data['count']
        f.write(f"Pollutant: {pollutant}\n")
        f.write(f"  Average AQI: {avg_aqi:.2f}\n")
        f.write(f"  Average Temperature: {avg_temp:.2f} °F\n\n")
    f.write(f" Average Temp From Weather: {average_temp} \n")
    f.write(f" Avergae Humidity From Weather: {average_humidity} \n")
    f.write(f" Average Pressure From Weather: {average_pressure} \n")


