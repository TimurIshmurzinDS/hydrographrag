import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data_snow = {
    'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
    'snow_depth': [5, 7, 6],
    'latitude': [48.9, 48.9, 48.9],
    'longitude': [116.4, 116.4, 116.4]
}

data_floods = {
    'date': ['2023-01-01', '2023-01-02', '2023-01-03'],
    'flood_level': [1.5, 2.0, 1.8],
    'latitude': [48.9, 48.9, 48.9],
    'longitude': [116.4, 116.4, 116.4]
}

# Преобразование данных в DataFrame
df_snow = pd.DataFrame(data_snow)
df_floods = pd.DataFrame(data_floods)

# Объединение данных по дате и координатам
merged_data = pd.merge(df_snow, df_floods, on=['date', 'latitude', 'longitude'])

# Вычисление корреляции
correlation = merged_data['snow_depth'].corr(merged_data['flood_level'])
print(f"Корреляция между снеготаянием и паводками: {correlation}")

# Создание карты
m = folium.Map(location=[48.9, 116.4], zoom_start=10)

# Добавление точек для снеготаяния
for index, row in df_snow.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Снеготаяние: {row['snow_depth']} см",
        icon=folium.Icon(color='blue', icon='cloud-snow')
    ).add_to(m)

# Добавление точек для паводков
for index, row in df_floods.iterrows():
    folium.Marker(
        location=[row['latitude'], row['longitude']],
        popup=f"Паводок: {row['flood_level']} м",
        icon=folium.Icon(color='red', icon='water')
    ).add_to(m)

# Сохранение карты
m.save("162.html")