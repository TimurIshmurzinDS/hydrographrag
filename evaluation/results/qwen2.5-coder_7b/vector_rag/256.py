import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile файла с границами ручья
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Определение центральной точки для карты
centroid = basin_data.geometry.centroid[0]

# Создание карты с центром в центре ручья и использованием тайла 'CartoDB positron'
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление границ ручья на карту
folium.GeoJson(basin_data.geometry.to_json(), 
                style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка координат городов (предполагается, что это WKT)
cities = [
    {"name": "г. Talgar", "wkt": "POINT(45.123456 78.901234)"}
]

# Добавление точек городов на карту
for city in cities:
    point = wkt.loads(city["wkt"])
    folium.Marker([point.y, point.x], popup=city["name"]).add_to(m)

# Сохранение карты в файл "256.html"
m.save("256.html")