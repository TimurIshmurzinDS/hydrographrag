import pandas as pd
from folium import Map, Marker
from folium.plugins import HeatMap

# Подключение к базе данных (в данном случае мы используем SQLite)
import sqlite3
conn = sqlite3.connect('geodb.db')

# Извлечение данных о датчиках уровня для рек Tentek River и Temirlik River
query = """
    SELECT 
        river_name, 
        sensor_level, 
        latitude, 
        longitude 
    FROM 
        sensors 
    WHERE 
        river_name IN ('Tentek River', 'Temirlik River')
"""
df = pd.read_sql_query(query, conn)

# Анализ данных и поиск аномалий (в данном случае мы просто выводим среднее значение уровня)
mean_level = df['sensor_level'].mean()
print(f"Средний уровень воды: {mean_level}")

# Визуализация результатов на карте
m = Map(location=[df['latitude'].mean(), df['longitude'].mean()], zoom_start=10)

for index, row in df.iterrows():
    Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Река: {row['river_name']}\nУровень воды: {row['sensor_level']}",
    ).add_to(m)

HeatMap(
    data=df[['latitude', 'longitude']].values,
    radius=10,
).add_to(m)

# Сохранение карты в файл
m.save("72.html")