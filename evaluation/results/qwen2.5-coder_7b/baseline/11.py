import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о глубине воды в Koktal River (в метрах)
data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [40.123, 45.678]  # Пример координат точки
            },
            "properties": {
                "time": "2023-04-10T12:00:00Z",  # Время измерения
                "depth": 1.5  # Глубина воды в метрах
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [40.124, 45.679]  # Пример координат точки
            },
            "properties": {
                "time": "2023-04-10T12:00:00Z",  # Время измерения
                "depth": 1.8  # Глубина воды в метрах
            }
        }
    ]
}

# Создание карты
m = folium.Map(location=[45.678, 40.123], zoom_start=12)

# Добавление слоя с отметками глубины воды
TimestampedGeoJson(data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты
m.save("11.html")

print("Карта сохранена как 11.html")