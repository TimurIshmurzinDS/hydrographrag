import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах из файла shapefile
basins = gpd.read_file(r"data/basin_data.shp")
basins = basins.to_crs(epsg=4326)

# Инициализация карты с центром в среднем значении координат бассейнов
centroid = basins.geometry.centroid.unary_union.centroid
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейнов на карту
folium.GeoJson(basins, style_function=lambda feature: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2,
}).add_to(m)

# Пример координат датчиков (WKT), если они есть в контексте
sensors = [
    {'name': 'Sensor1', 'wkt': 'POINT(75.934 42.867)', 'status': 'OK'},
    {'name': 'Sensor2', 'wkt': '75.940 42.870', 'status': 'Faulty'},
    # Добавьте другие датчики по аналогии
]

# Добавление маркеров на карту для каждого датчика
for sensor in sensors:
    point = wkt.loads(sensor['wkt'])
    folium.Marker(
        location=[point.y, point.x],
        popup=f"{sensor['name']} - {sensor['status']}",
        icon=folium.Icon(color='red' if sensor['status'] == 'Faulty' else 'green')
    ).add_to(m)

# Сохранение карты в файл
m.save("137.html")