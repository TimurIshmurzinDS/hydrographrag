import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile и конвертация в CRS 'EPSG:4326'
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром на centroid shapefile
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границы бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты для речек Byzhy River и Lepsy River (пример)
rivers = [
    {"name": "Byzhy River", "wkt": "LINESTRING(37.123456 48.987654, 37.123456 48.987654)"},
    {"name": "Lepsy River", "wkt": "LINESTRING(37.123456 48.987654, 37.123456 48.987654)"}
]

# Добавление речек на карту
for river in rivers:
    geom = wkt.loads(river["wkt"])
    folium.GeoJson(geom, style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

# Сохранение карты в файл
m.save("109.html")