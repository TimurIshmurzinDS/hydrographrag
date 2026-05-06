import folium
from folium.plugins import TimestampedGeoJson

# Сбор данных о уровне воды в реке (для примера использованы фиктивные данные)
data = {
    "type": "FeatureCollection",
    "features": [
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [37.615, 55.755]
            },
            "properties": {
                "time": "2023-03-01T12:00:00Z",
                "water_level": 1.2
            }
        },
        {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [37.620, 55.760]
            },
            "properties": {
                "time": "2023-03-01T13:00:00Z",
                "water_level": 1.5
            }
        }
    ]
}

# Создание географической модели реки (для примера использована фиктивная модель)
model = folium.Map(location=[55.755, 37.615], zoom_start=12)

# Интеграция данных о текущем уровне воды в реку с географической моделью
timestamped_geojson = TimestampedGeoJson(
    data,
    period="PT1H",  # период времени между двумя последовательными точками данных (в данном случае - час)
    add_last_point=True,  # добавление последней точки данных на карте
    auto_play=False,  # автоматический запуск анимации
    loop=False,  # повторение анимации
    max_speed=1  # максимальная скорость анимации (в данном случае - 1 час в секунду)
)

# Визуализация результатов на карте
model.add_child(timestamped_geojson)

# Сохранение карты в файл
m = model
m.save("5.html")