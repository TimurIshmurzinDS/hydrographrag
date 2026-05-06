import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs(epsg=4326)

# Создание карты с центром в центроиде водного бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть следующие данные о датчиках (координаты в формате WKT)
sensors = [
    {"name": "Sensor1", "wkt": "POINT(76.95 43.02)", "status": "Активен"},
    {"name": "Sensor2", "wkt": "POINT(76.98 43.05)", "status": "Неактивен"},
    {"name": "Sensor3", "wkt": "POINT(77.01 43.03)", "status": "Активен"}
]

# Добавление маркеров на карту
for sensor in sensors:
    point = wkt.loads(sensor["wkt"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"Датчик: {sensor['name']}, Статус: {sensor['status']}",
        icon=folium.Icon(color='blue' if sensor['status'] == 'Активен' else 'red')
    ).add_to(m)

# Сохранение карты в файл
m.save("10.html")