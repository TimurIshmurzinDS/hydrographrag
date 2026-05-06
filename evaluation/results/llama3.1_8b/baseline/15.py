import folium
from folium.plugins import TimestampedGeoJson

# Подготовка географической информации о реке и ее бассейне
river_coords = [
    [43.1234, 76.5678],  # Координаты точки на берегу
    [43.2345, 76.6789],
    [43.3456, 76.7890]
]

# Подготовка данных о уровне воды в реальном времени
water_level_data = [
    {"time": "2023-02-20T12:00:00", "level": 10},
    {"time": "2023-02-20T13:00:00", "level": 11},
    {"time": "2023-02-20T14:00:00", "level": 12}
]

# Создание модели геообработки
def create_geojson(data):
    geojson = {
        "type": "FeatureCollection",
        "features": []
    }
    
    for point in river_coords:
        feature = {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": [point[1], point[0]]
            },
            "properties": {
                "time": data["time"],
                "level": data["level"]
            }
        }
        geojson["features"].append(feature)
    
    return geojson

# Создание карты с текущим уровнем воды
m = folium.Map(location=[43.2, 76.5], zoom_start=12)

geojson_data = create_geojson(water_level_data[0])
TimestampedGeoJson(geojson_data).add_to(m)

# Сохранение карты в файл
m.save("15.html")