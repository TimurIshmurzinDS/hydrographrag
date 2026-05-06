import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о уровне воды (в метрах)
water_level_data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [76.9234, 43.1234]  # Координаты точки на риере
            },
            "properties": {
                "time": "2023-04-15T12:00:00Z",
                "level": 1.5  # Уровень воды в метрах
            }
        }
    ]
}

# Создание карты Ulken Almaty River
m = folium.Map(location=[43.1234, 76.9234], zoom_start=10)

# Добавление слоя с отметкой уровня воды
TimestampedGeoJson(water_level_data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты в файл
m.save("15.html")

print("Карта сохранена как 15.html")