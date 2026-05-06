import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о уровне воды (в метрах над уровнем моря)
water_levels = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [37.1234, 55.6789]},
            "properties": {
                "time": "2023-04-10T12:00:00Z",
                "level": 1.5
            }
        },
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [37.1236, 55.6790]},
            "properties": {
                "time": "2023-04-10T12:00:00Z",
                "level": 1.8
            }
        },
        # Добавьте больше точек с уровнями воды по мере необходимости
    ]
}

# Создание карты
m = folium.Map(location=[55.6790, 37.1234], zoom_start=13)

# Визуализация данных о уровне воды на карте
TimestampedGeoJson(water_levels, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты в файл
m.save("5.html")