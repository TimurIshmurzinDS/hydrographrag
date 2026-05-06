import folium
from folium.plugins import TimestampedGeoJson

# Сбор данных о реке Шижин и ее гидрологических характеристиках.
# Для простоты предположим, что данные находятся в формате GeoJSON.
river_data = {
    "type": "Feature",
    "geometry": {
        "type": "LineString",
        "coordinates": [
            [48.6784, 35.0333],
            [48.6822, 35.0389]
        ]
    },
    "properties": {
        "name": "Shyzhyn River"
    }
}

# Получение данных о уровнях воды в реке на данный момент времени.
water_level_data = [
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [48.6784, 35.0333]}, "properties": {"level": 10}},
    {"type": "Feature", "geometry": {"type": "Point", "coordinates": [48.6822, 35.0389]}, "properties": {"level": 12}}
]

# Анализ полученных данных для определения превышения нормального уровня воды.
normal_level = 11
exceeded_points = []
for point in water_level_data:
    if point["properties"]["level"] > normal_level:
        exceeded_points.append(point)

# Если превышен нормальный уровень воды, то необходимо определить ближайшие населенные пункты и оповестить их об опасности.
if exceeded_points:
    # Для простоты предположим, что данные о населенных пунктах находятся в формате GeoJSON.
    population_data = {
        "type": "FeatureCollection",
        "features": [
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [48.6800, 35.0355]}, "properties": {"name": "City1"}},
            {"type": "Feature", "geometry": {"type": "Point", "coordinates": [48.6850, 35.0400]}, "properties": {"name": "City2"}}
        ]
    }

    # Создание карты с маркерами для превышения нормального уровня воды и ближайших населенных пунктов.
    m = folium.Map(location=[48.6800, 35.0355], zoom_start=12)
    for point in exceeded_points:
        folium.Marker(point["geometry"]["coordinates"], popup=f"Уровень воды: {point['properties']['level']}").add_to(m)
    for city in population_data["features"]:
        folium.Marker(city["geometry"]["coordinates"], popup=city["properties"]["name"]).add_to(m)

    # Сохранение карты в файл.
    m.save("28.html")
else:
    print("Нет превышения нормального уровня воды.")