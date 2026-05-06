import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs('EPSG:4326')

# Создание карты с центром в бассейне
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о датчиках уровня воды (координаты в формате WKT)
sensor_data = [
    {"name": "Sensor1", "wkt": "POINT(37.618423 55.755814)", "water_level_value": 150, "date_water_level_value": "2023-10-01"},
    {"name": "Sensor2", "wkt": "POINT(37.628423 55.765814)", "water_level_value": 160, "date_water_level_value": "2023-10-01"},
    {"name": "Sensor3", "wkt": "POINT(37.638423 55.775814)", "water_level_value": 170, "date_water_level_value": "2023-10-01"}
]

# Добавление точек датчиков на карту
for sensor in sensor_data:
    point = wkt.loads(sensor["wkt"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Датчик: {sensor['name']}, Уровень воды: {sensor['water_level_value']} см, Дата: {sensor['date_water_level_value']}",
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты
m.save("136.html")