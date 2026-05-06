import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна из shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с использованием центра масс бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат мониторинговых точек и их значений
monitoring_points = [
    {"name": "Точка 1", "wkt": "POINT(37.5648 55.7558)", "value": 1.7},
    {"name": "Точка 2", "wkt": "POINT(37.5649 55.7559)", "value": 1.7},
    {"name": "Точка 3", "wkt": "POINT(37.5650 55.7560)", "value": 1.7}
]

# Добавление мониторинговых точек на карту
for point in monitoring_points:
    geom = wkt.loads(point["wkt"])
    folium.Marker([geom.y, geom.x], popup=f"{point['name']}: {point['value']} km").add_to(m)

# Сохранение карты в файл
m.save("142.html")