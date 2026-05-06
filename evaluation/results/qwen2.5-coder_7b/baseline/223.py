import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о уровне воды (замените на реальные данные)
data = {
    'timestamp': ['2023-10-01', '2023-10-02', '2023-10-03'],
    'latitude': [54.67, 54.68, 54.69],
    'longitude': [86.12, 86.13, 86.14],
    'water_level': [100, 105, 95]
}

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование времени в datetime
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Определение критических уровней воды
critical_levels = {
    'low': 90,
    'high': 110
}

# Создание карты
m = folium.Map(location=[54.68, 86.13], zoom_start=12)

# Добавление точек с уровнями воды на карту
for index, row in df.iterrows():
    if row['water_level'] < critical_levels['low']:
        color = 'red'
    elif row['water_level'] > critical_levels['high']:
        color = 'green'
    else:
        color = 'blue'
    
    folium.CircleMarker(
        location=[row['latitude'], row['longitude']],
        radius=10,
        popup=f"Water Level: {row['water_level']} m",
        color=color,
        fill=True,
        fill_color=color
    ).add_to(m)

# Добавление критических уровней на карту
folium.CircleMarker(
    location=[54.68, 86.13],
    radius=10,
    popup=f"Critical Level: Low {critical_levels['low']} m",
    color='red',
    fill=True,
    fill_color='red'
).add_to(m)

folium.CircleMarker(
    location=[54.68, 86.13],
    radius=10,
    popup=f"Critical Level: High {critical_levels['high']} m",
    color='green',
    fill=True,
    fill_color='green'
).add_to(m)

# Сохранение карты
m.save("223.html")