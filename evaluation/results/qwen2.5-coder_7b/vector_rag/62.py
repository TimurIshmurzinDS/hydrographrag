import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат для постов мониторинга (если они доступны)
monitoring_posts = [
    {"name": "Post1", "wkt": "POINT(55.755864 37.617298)", "status": False},
    {"name": "Post2", "wkt": "POINT(55.755864 37.617298)", "status": True},
    {"name": "Post3", "wkt": "POINT(55.755864 37.617298)", "status": False}
]

# Добавление маркеров постов мониторинга на карту
for post in monitoring_posts:
    point = wkt.loads(post["wkt"])
    folium.Marker([point.y, point.x], popup=post["name"], icon=folium.Icon(color='red' if not post["status"] else 'green')).add_to(m)

# Сохранение карты в файл
m.save("62.html")