import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейнах из shapefile
basins = gpd.read_file(r"data/basin_data.shp")
basins = basins.to_crs('EPSG:4326')

# Инициализация карты с центроидом бассейнов
centroid = basins.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basins.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если есть координаты (WKT), создаем список словарей
coordinates = [
    {"name": "Sarykan River Confluence", "wkt": "POINT(0 0)"},  # Примерные координаты, заменить на реальные
    {"name": "Emel River Confluence", "wkt": "POINT(0 0)"}     # Примерные координаты, заменить на реальные
]

# Добавление точек на карту
for coord in coordinates:
    point = wkt.loads(coord["wkt"])
    folium.Marker([point.y, point.x], popup=coord["name"]).add_to(m)

# Сохранение карты в файл
m.save("177.html")