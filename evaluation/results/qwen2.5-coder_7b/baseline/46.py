import pandas as pd
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data_2022 = {
    'latitude': [43.123, 43.456, 43.789],
    'longitude': [76.123, 76.456, 76.789],
    'water_level_2022': [100, 120, 110]
}

data_2023 = {
    'latitude': [43.123, 43.456, 43.789],
    'longitude': [76.123, 76.456, 76.789],
    'water_level_2023': [110, 130, 120]
}

# Создание DataFrame
df_2022 = pd.DataFrame(data_2022)
df_2023 = pd.DataFrame(data_2023)

# Объединение данных в один DataFrame
merged_data = pd.merge(df_2022, df_2023, on=['latitude', 'longitude'], suffixes=('_2022', '_2023'))

# Создание карты
m = folium.Map(location=[43.5, 76.5], zoom_start=10)

# Добавление слоев данных для каждого года
TimestampedGeoJson({
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            },
            "properties": {
                "time": f"2022-01-01T00:00:00Z",
                "water_level": row['water_level_2022'],
                "color": "blue"
            }
        } for index, row in merged_data.iterrows()
    ]
}).add_to(m)

TimestampedGeoJson({
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [row['longitude'], row['latitude']]
            },
            "properties": {
                "time": f"2023-01-01T00:00:00Z",
                "water_level": row['water_level_2023'],
                "color": "red"
            }
        } for index, row in merged_data.iterrows()
    ]
}).add_to(m)

# Сохранение карты
m.save("46.html")