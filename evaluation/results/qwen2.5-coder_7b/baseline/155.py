import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Загрузка данных
data_bayankol = pd.read_csv('bayankol_river_data.csv')
data_lepsy = pd.read_csv('lepsy_river_data.csv')

# Пример структуры данных:
# data_bayankol = {
#     'date': ['2023-04-01', '2023-04-02', ...],
#     'water_level': [5.2, 5.3, ...]
# }

# Пример структуры данных:
# data_lepsy = {
#     'date': ['2023-04-01', '2023-04-02', ...],
#     'water_level': [6.1, 6.2, ...]
# }

# Преобразование дат в формат datetime
data_bayankol['date'] = pd.to_datetime(data_bayankol['date'])
data_lepsy['date'] = pd.to_datetime(data_lepsy['date'])

# Обработка данных (пример: удаление пропущенных значений)
data_bayankol.dropna(inplace=True)
data_lepsy.dropna(inplace=True)

# Создание карты
m = folium.Map(location=[50.1, 86.2], zoom_start=7)

# Формирование GeoJSON для визуализации данных
geojson_bayankol = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [86.2, 50.1]  # Пример координат
            },
            "properties": {
                "time": data_bayankol['date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').tolist(),
                "water_level": data_bayankol['water_level'].tolist()
            }
        }
    ]
}

geojson_lepsy = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [86.2, 50.1]  # Пример координат
            },
            "properties": {
                "time": data_lepsy['date'].dt.strftime('%Y-%m-%dT%H:%M:%SZ').tolist(),
                "water_level": data_lepsy['water_level'].tolist()
            }
        }
    ]
}

# Добавление данных на карту
TimestampedGeoJson(geojson_bayankol, period="PT1H", add_last_point=True).add_to(m)
TimestampedGeoJson(geojson_lepsy, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("155.html")