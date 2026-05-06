import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о водном бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в центроиде водного бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ водного бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат датчиков (WKT)
sensor_locations = [
    {"name": "Sensor A1", "river": "Aksu River", "wkt": "POINT(76.9345 42.8820)", "status": "Работает"},
    {"name": "Sensor A2", "river": "Aksu River", "wkt": "POINT(76.9410 42.8850)", "status": "Неисправен"},
    {"name": "Sensor K1", "river": "Koktal River", "wkt": "POINT(76.9280 42.8900)", "status": "Работает"},
    {"name": "Sensor K2", "river": "Koktal River", "wkt": "POINT(76.9350 42.8950)", "status": "Неисправен"}
]

# Добавление маркеров датчиков на карту
for sensor in sensor_locations:
    point = wkt.loads(sensor["wkt"])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"{sensor['name']} на {sensor['river']}, Статус: {sensor['status']}",
        icon=folium.Icon(color='blue' if sensor['status'] == 'Работает' else 'red')
    ).add_to(m)

# Сохранение карты в файл
m.save("69.html")