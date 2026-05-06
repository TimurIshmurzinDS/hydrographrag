import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
dos_river_data = pd.read_csv('dos_river_data.csv')
kurty_river_data = pd.read_csv('kurty_river_data.csv')

# Пример структуры данных:
# dos_river_data: ['date', 'flow']
# kurty_river_data: ['date', 'flow']

# Преобразование дат в формат datetime
dos_river_data['date'] = pd.to_datetime(dos_river_data['date'])
kurty_river_data['date'] = pd.to_datetime(kurty_river_data['date'])

# Анализ временных рядов
dos_river_flow_mean = dos_river_data.groupby(dos_river_data['date'].dt.year)['flow'].mean()
kurty_river_flow_mean = kurty_river_data.groupby(kurty_river_data['date'].dt.year)['flow'].mean()

# Сравнение осадков и стоков
recent_precipitation = pd.read_csv('recent_precipitation.csv')
recent_precipitation['date'] = pd.to_datetime(recent_precipitation['date'])

# Пример структуры данных:
# recent_precipitation: ['date', 'precipitation']

# Визуализация на карте
m = folium.Map(location=[50, 15], zoom_start=6)

# Добавление точек для реки Dos River
dos_river_geojson = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in dos_river_data.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": row['date'].isoformat(),
            "flow": row['flow']
        }
    }
    dos_river_geojson["features"].append(feature)

TimestampedGeoJson(dos_river_geojson, period="PT1D", add_last_point=True).add_to(m)

# Добавление точек для реки Kurty River
kurty_river_geojson = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in kurty_river_data.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": row['date'].isoformat(),
            "flow": row['flow']
        }
    }
    kurty_river_geojson["features"].append(feature)

TimestampedGeoJson(kurty_river_geojson, period="PT1D", add_last_point=True).add_to(m)

# Добавление точек для недавних осадков
precipitation_geojson = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in recent_precipitation.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": row['date'].isoformat(),
            "precipitation": row['precipitation']
        }
    }
    precipitation_geojson["features"].append(feature)

TimestampedGeoJson(precipitation_geojson, period="PT1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("133.html")