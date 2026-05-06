import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат датчиков (если они есть)
sensor_coordinates = [
    {"name": "Karatal River Sensor", "wkt": "POINT(45.1234 78.9012)"}
]

# Добавление точек сенсоров на карту
for sensor in sensor_coordinates:
    point = wkt.loads(sensor["wkt"])
    folium.Marker([point.y, point.x], popup=sensor["name"]).add_to(m)

# Сохранение карты в файл
m.save("222.html")