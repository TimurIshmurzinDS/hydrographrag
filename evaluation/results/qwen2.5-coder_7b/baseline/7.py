import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о текущем уровне воды в реке Batareyka River
data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [37.1234, 56.7890]  # Пример координат точки на берегу реки
            },
            "properties": {
                "time": "2023-04-10T12:00:00Z",
                "level": 1.5  # Уровень воды в метрах
            }
        }
    ]
}

# Создание карты
m = folium.Map(location=[56.7890, 37.1234], zoom_start=12)

# Добавление слоя с отметками уровня воды
TimestampedGeoJson(data, period="PT1H", add_last_point=True).add_to(m)

# Сохранение карты в файл
m.save("7.html")