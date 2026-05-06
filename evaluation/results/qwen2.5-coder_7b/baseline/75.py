import folium
from folium.plugins import TimestampedGeoJson

# Пример данных о течении рек (скорость и направление)
tentek_river_data = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [50.1, 49.2]}, "properties": {"speed": 3, "direction": "N"}},
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [50.2, 49.3]}, "properties": {"speed": 2, "direction": "NE"}}
    ]
}

sharyn_river_data = {
    "type": "FeatureCollection",
    "features": [
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [50.15, 49.25]}, "properties": {"speed": 3, "direction": "S"}},
        {"type": "Feature", "geometry": {"type": "Point", "coordinates": [50.25, 49.35]}, "properties": {"speed": 2, "direction": "SE"}}
    ]
}

# Создание карты
m = folium.Map(location=[50.175, 49.3], zoom_start=12)

# Добавление данных о течении рек на карту
TimestampedGeoJson(tentek_river_data, period="PT1M", add_last_point=True).add_to(m)
TimestampedGeoJson(sharyn_river_data, period="PT1M", add_last_point=True).add_to(m)

# Добавление маркеров для обозначения направления течения
for feature in tentek_river_data["features"]:
    folium.Marker(feature["geometry"]["coordinates"], popup=f"Tentek River - Speed: {feature['properties']['speed']} km/h, Direction: {feature['properties']['direction']}", icon=folium.Icon(color='blue')).add_to(m)

for feature in sharyn_river_data["features"]:
    folium.Marker(feature["geometry"]["coordinates"], popup=f"Sharyn River - Speed: {feature['properties']['speed']} km/h, Direction: {feature['properties']['direction']}", icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("75.html")