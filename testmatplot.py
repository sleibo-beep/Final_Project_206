import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

# Connect to DB
conn = sqlite3.connect('final_project.db')
query = '''
    SELECT zip, AVG(aqi) AS avg_aqi
    FROM AirQualityData
    GROUP BY zip
    ORDER BY zip
'''
df = pd.read_sql_query(query, conn)
conn.close()

# Treat ZIP codes as strings for display
df['zip'] = df['zip'].astype(str)

# Generate even spacing for x-axis
x_positions = range(len(df))

# Increase width physically for the interactive graph
plt.figure(figsize=(16, 6))  # Widen the plot (physically larger interactive view)
plt.plot(x_positions, df['avg_aqi'], marker='o', linestyle='-', color='teal')
plt.xticks(ticks=x_positions, labels=df['zip'], rotation=90)

# Add labels
plt.xlabel('Zip Code')
plt.ylabel('Average AQI')
plt.title('Average AQI by Zip Code')
plt.grid(True)

# Add left margin to prevent cutting off the y-axis
plt.subplots_adjust(left=0.15)

# Show plot
plt.show()
