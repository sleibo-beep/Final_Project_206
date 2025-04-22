import sqlite3
import pandas as pd
import matplotlib.pyplot as plt

conn = sqlite3.connect('final_project.db')
query = '''
    SELECT zip, AVG(aqi) AS avg_aqi
    FROM AirQualityData
    GROUP BY zip
    ORDER BY zip
'''
df = pd.read_sql_query(query, conn)
conn.close()

df['zip'] = df['zip'].astype(str)

x_positions = range(len(df))

plt.figure(figsize=(20, 6))  

plt.plot(x_positions, df['avg_aqi'], marker='o', linestyle='-', color='teal')


step = max(1, len(df) // 25) 
plt.xticks(
    ticks=[i for i in x_positions if i % step == 0],
    labels=[df['zip'][i] for i in range(len(df)) if i % step == 0],
    rotation=45,
    ha='right'
)

plt.xlabel('Zip Code')
plt.ylabel('Average AQI')
plt.title('Average AQI by Zip Code')
plt.grid(True)

plt.tight_layout()

plt.show()