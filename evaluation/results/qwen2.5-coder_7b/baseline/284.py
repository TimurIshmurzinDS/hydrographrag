import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных: загрузка исторических данных о климате на Марсе
data = {
    'latitude': [18.0, 20.0, 22.0, 24.0],
    'longitude': [-75.0, -73.0, -71.0, -69.0],
    'temperature': [20, 22, 24, 26],
    'pressure': [800, 820, 840, 860]
}
df = pd.DataFrame(data)

# Создание карты
m = folium.Map(location=[21.0, -75.0], zoom_start=3)

# Преобразование данных в формат для TimestampedGeoJson
geojson_data = {
    "type": "FeatureCollection",
    "features": []
}

for index, row in df.iterrows():
    feature = {
        "type": "Feature",
        "geometry": {
            "type": "Point",
            "coordinates": [row['longitude'], row['latitude']]
        },
        "properties": {
            "time": f"2023-01-{index+1}T00:00:00Z",  # Пример времени
            "temperature": row['temperature'],
            "pressure": row['pressure']
        }
    }
    geojson_data["features"].append(feature)

# Добавление слоя с временной геоданныей
TimestampedGeoJson(geojson_data, period="PT1D", add_last_point=True).add_to(m)

# Сохранение карты
m.save("284.html")