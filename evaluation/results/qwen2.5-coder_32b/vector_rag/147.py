import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне рек из файла shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположительные координаты датчиков в формате WKT (для демонстрации)
sensors = [
    {"name": "Sensor1", "wkt": "POINT(45.3456 40.1234)", "status": "OK"},
    {"name": "Sensor2", "wkt": "POINT(45.3567 40.1345)", "status": "ERROR"},
    {"name": "Sensor3", "wkt": "POINT(45.3678 40.1456)", "status": "OK"}
]

# Добавление датчиков на карту
for sensor in sensors:
    point = wkt.loads(sensor["wkt"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"{sensor['name']}: {sensor['status']}",
        icon=folium.Icon(color='green' if sensor['status'] == 'OK' else 'red')
    ).add_to(m)

# Сохранение карты в файл
m.save("147.html")