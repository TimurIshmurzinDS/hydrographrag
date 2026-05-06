import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о уровне воды на реке Osek River (замените на реальные данные)
data = {
    'timestamp': ['2023-10-01 08:00', '2023-10-01 09:00', '2023-10-01 10:00'],
    'latitude': [54.67, 54.67, 54.67],
    'longitude': [38.12, 38.13, 38.14],
    'water_level': [1.2, 1.5, 1.8]
}

# Создание DataFrame
df = pd.DataFrame(data)
df['timestamp'] = pd.to_datetime(df['timestamp'])

# Создание карты
m = folium.Map(location=[54.67, 38.12], zoom_start=10)

# Добавление точек с уровнями воды на карте
for index, row in df.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Уровень воды: {row['water_level']} м",
        icon=folium.Icon(color='red', icon='info-sign')
    ).add_to(m)

# Сохранение карты
m.save("26.html")