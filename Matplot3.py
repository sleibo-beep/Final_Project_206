import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to the database and get joined data
conn = sqlite3.connect("final_project.db")
df = pd.read_sql_query("SELECT * FROM WeatherAirQualityJoin", conn)
conn.close()

# Basic scatter plot
plt.figure(figsize=(10, 6))
plt.scatter(df['temp'], df['aqi'], color='teal', alpha=0.7)

# Labels and title
plt.xlabel('Temperature (°F)')
plt.ylabel('Air Quality Index (AQI)')
plt.title('Temperature vs. AQI')

plt.grid(True)
plt.tight_layout()
plt.show()
