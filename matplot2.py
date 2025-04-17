import sqlite3
import matplotlib.pyplot as plt

conn = sqlite3.connect('final_project.db')
cursor = conn.cursor()

cursor.execute("SELECT AVG(aqi) FROM AirQualityData")
average_aqi = cursor.fetchone()[0]

print("Average Temp:", average_aqi)


conn.close()

fig = plt.figure(figsize=(10,5))
ax1 = fig.add_subplot(221)
ax1.set_xlabel("AQI")
ax1.set_ylabel("Average")

# Plot the data
ax1.bar(["AQI"],[average_aqi])

# Show the plot
plt.show()
