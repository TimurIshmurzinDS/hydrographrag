import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о уровнях воды в реках Лепсы и Бутак (в формате GeoJSON)
lepsy_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [37.123, 55.432]},
            "properties": {"name": "Лепса", "water_level": 10}
        },
        # Добавьте другие точки для Лепсы
    ]
}

butak_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [37.456, 55.789]},
            "properties": {"name": "Бутак", "water_level": 12}
        },
        # Добавьте другие точки для Бутак
    ]
}

# Создание карты
m = folium.Map(location=[55.432, 37.123], zoom_start=10)

# Добавление слоев данных на карту
TimestampedGeoJson(lepsy_data, period="PT1H", add_last_point=True).add_to(m)
TimestampedGeoJson(butak_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты в файл
m.save("138.html")