import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Karaoy River из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центральной точки shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ ручья на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример данных о уровне воды (если есть)
water_level_data = [
    {'name': 'Sensor1', 'wkt': 'POINT(37.5648 40.7128)', 'level': 10},
    {'name': 'Sensor2', 'wkt': 'POINT(37.5650 40.7130)', 'level': 12}
]

# Добавление точек с уровнями воды на карту
for sensor in water_level_data:
    point = wkt.loads(sensor['wkt'])
    folium.Marker([point.y, point.x], popup=f"{sensor['name']}: Уровень {sensor['level']}").add_to(m)

# Сохранение карты в файл
m.save("216.html")