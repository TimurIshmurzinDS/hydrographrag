import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных сенсоров (если доступны)
sensor_points = [
    {"name": "Sensor1", "wkt": "POINT(35.689487 139.691711)"},
    {"name": "Sensor2", "wkt": "POINT(35.690487 139.692711)"}
]

# Добавление точек сенсоров на карту
for sensor in sensor_points:
    point = wkt.loads(sensor["wkt"])
    folium.Marker([point.y, point.x], popup=sensor["name"]).add_to(m)

# Сохранение финальной карты
m.save("64.html")