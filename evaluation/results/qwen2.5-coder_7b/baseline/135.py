import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data_shilik = {
    'date': pd.date_range(start='2010-01-01', end='2020-12-31'),
    'water_level': np.random.uniform(5, 15, size=12*10)  # Случайные значения для демонстрации
}

data_sharyn = {
    'date': pd.date_range(start='2010-01-01', end='2020-12-31'),
    'water_level': np.random.uniform(5, 15, size=12*10)  # Случайные значения для демонстрации
}

df_shilik = pd.DataFrame(data_shilik)
df_sharyn = pd.DataFrame(data_sharyn)

# Пример координат для рек (замените на реальные данные)
shilik_coords = [(55.75, 37.61), (55.80, 37.62)]
sharyn_coords = [(55.76, 37.63), (55.77, 37.64)]

# Создание карты
m = folium.Map(location=[55.75, 37.61], zoom_start=10)

# Добавление данных о реках на карту
for coords in shilik_coords:
    folium.Marker(coords, popup='Shilik River').add_to(m)
    
for coords in sharyn_coords:
    folium.Marker(coords, popup='Sharyn River').add_to(m)

# Создание слоев для временных рядов
shilik_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coords},
            "properties": {
                "time": df_shilik['date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').values.tolist(),
                "value": df_shilik['water_level'].values.tolist()
            }
        } for coords in shilik_coords
    ]
}

sharyn_geojson = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coords},
            "properties": {
                "time": df_sharyn['date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').values.tolist(),
                "value": df_sharyn['water_level'].values.tolist()
            }
        } for coords in sharyn_coords
    ]
}

# Добавление слоев на карту
TimestampedGeoJson(shilik_geojson, period='P1D', add_last_point=True).add_to(m)
TimestampedGeoJson(sharyn_geojson, period='P1D', add_last_point=True).add_to(m)

# Сохранение карты
m.save("135.html")