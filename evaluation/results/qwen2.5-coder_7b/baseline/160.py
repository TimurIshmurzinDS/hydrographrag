import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных (замените на реальные данные)
data = {
    'date': pd.date_range(start='1/1/2020', periods=365, freq='D'),
    'Ili_River': np.random.randint(100, 500, size=365),
    'Shyzhyn_River': np.random.randint(100, 500, size=365)
}

# Создание DataFrame
df = pd.DataFrame(data)

# Пример координат для каждой реки (замените на реальные данные)
ili_coords = [(42.87, 74.57), (42.90, 74.60)]  # Примерные координаты
shyzhyn_coords = [(43.10, 74.70), (43.15, 74.80)]  # Примерные координаты

# Создание слоев для каждой реки
ili_layer = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coord},
            "properties": {"time": date.strftime('%Y-%m-%dT%H:%M:%SZ'), "value": level}
        }
        for date, level, coord in zip(df['date'], df['Ili_River'], ili_coords)
    ]
}

shyzhyn_layer = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": coord},
            "properties": {"time": date.strftime('%Y-%m-%dT%H:%M:%SZ'), "value": level}
        }
        for date, level, coord in zip(df['date'], df['Shyzhyn_River'], shyzhyn_coords)
    ]
}

# Создание карты
m = folium.Map(location=[42.985, 74.63], zoom_start=10)

# Добавление слоев на карту
TimestampedGeoJson(ili_layer, period="PT1D", add_last_point=True).add_to(m)
TimestampedGeoJson(shyzhyn_layer, period="PT1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("160.html")