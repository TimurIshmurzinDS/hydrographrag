import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о гидрологическом режиме реки Шарын и его влиянии на туризм
data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [74.5, 39.0]  # Пример координат точки на карте
            },
            "properties": {
                "name": "Шарын",
                "water_level_change": -10,  # Изменение уровня воды (в метрах)
                "ecological_impact": "Ухудшение качества воды",
                "tourism_impact": "Ограничение доступности для плавания"
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [74.6, 39.1]  # Пример координат точки на карте
            },
            "properties": {
                "name": "Шарын",
                "water_level_change": 5,  # Изменение уровня воды (в метрах)
                "ecological_impact": "Улучшение качества воды",
                "tourism_impact": "Повышение доступности для плавания"
            }
        }
    ]
}

# Создание карты
m = folium.Map(location=[39.0, 74.5], zoom_start=12)

# Добавление слоя с гидрологическими данными и их влиянием на туризм
TimestampedGeoJson(data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты в файл
m.save("194.html")