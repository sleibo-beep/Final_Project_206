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

# --- PLOT SETUP ---
plt.figure(figsize=(20, 6))  # Wider figure

# Line plot
plt.plot(x_positions, df['avg_aqi'], marker='o', linestyle='-', color='teal')

# Limit how many ZIP labels are shown on x-axis
# Show every Nth ZIP code label
step = max(1, len(df) // 25)  # Show ~25 labels max
plt.xticks(
    ticks=[i for i in x_positions if i % step == 0],
    labels=[df['zip'][i] for i in range(len(df)) if i % step == 0],
    rotation=45,
    ha='right'
)

# Labels & Title
plt.xlabel('Zip Code')
plt.ylabel('Average AQI')
plt.title('Average AQI by Zip Code')
plt.grid(True)

# Adjust spacing so labels don't get cut off
plt.tight_layout()

# Show plot
plt.show()