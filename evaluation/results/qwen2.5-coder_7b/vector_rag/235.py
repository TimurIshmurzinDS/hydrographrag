import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и преобразование в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центра масс shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление базины на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат для запуска спутника (пример)
launch_points = [
    {"name": "Point A", "wkt": "POINT(45.1234 78.9012)"},
    {"name": "Point B", "wkt": "POINT(46.1234 79.9012)"}
]

# Преобразование WKT в координаты и добавление маркеров на карту
for point in launch_points:
    geom = wkt.loads(point["wkt"])
    folium.Marker([geom.y, geom.x], popup=point["name"]).add_to(m)

# Добавление точек измерения расхода воды
water_consumption_points = [
    {"name": "Point 1", "wkt": "POINT(45.2345 78.0123)"},
    {"name": "Point 2", "wkt": "POINT(46.2345 79.0123)"},
    {"name": "Point 3", "wkt": "POINT(47.2345 78.0123)"}
]

for point in water_consumption_points:
    geom = wkt.loads(point["wkt"])
    folium.Marker([geom.y, geom.x], popup=point["name"], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("235.html")