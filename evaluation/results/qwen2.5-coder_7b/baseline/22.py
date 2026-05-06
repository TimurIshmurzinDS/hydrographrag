import pandas as pd
import numpy as np
import folium
from folium.plugins import TimestampedGeoJson

# Пример данных: дата, уровень воды (в метрах)
data = {
    'date': ['2023-04-01', '2023-04-02', '2023-04-03', '2023-04-04', '2023-04-05'],
    'water_level': [1.2, 1.5, 2.0, 2.5, 3.0]
}

# Преобразование данных в DataFrame
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Определение пикового уровня воды
peak_water_level = df['water_level'].max()
peak_date = df[df['water_level'] == peak_water_level]['date'].values[0]

print(f"Пиковый уровень воды: {peak_water_level} м")
print(f"Дата пика: {peak_date}")

# Визуализация данных на карте
m = folium.Map(location=[42.1697, 73.5856], zoom_start=10)  # Координаты примера (Uzyn Kargaly River)

# Создание GeoJSON для визуализации пиков уровня воды
geojson_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [73.5856, 42.1697]  # Координаты примера (Uzyn Kargaly River)
            },
            "properties": {
                "time": peak_date.strftime('%Y-%m-%dT%H:%M:%SZ'),
                "title": f"Пиковый уровень воды: {peak_water_level} м",
                "icon": "circle",
                "iconstyle": {
                    "fillColor": "#ff0000",
                    "fillOpacity": 1,
                    "stroke": False
                }
            }
        }
    ]
}

# Добавление GeoJSON на карту
TimestampedGeoJson(geojson_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("22.html")