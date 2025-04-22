import sqlite3
import matplotlib.pyplot as plt

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

# Initialize the plot
fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(221)
ax1.set_xlabel("Weather Statistic")
ax1.set_ylabel("Average Per Zipcode")
ax1.set_title("Average Weather Statistics Per Zipcode")

# Plot the data
ax1.bar(["Temp (°F)","Pressure (inHg)","Humidity (%)"],[average_temp,average_pressure,average_humidity])

# Show the plot
plt.show()
