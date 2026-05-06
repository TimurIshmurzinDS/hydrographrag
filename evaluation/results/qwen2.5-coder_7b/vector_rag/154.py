import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (если необходимо)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат для рек (если они есть в WKT формате)
river_coords = [
    {"name": "Shynzhaly River", "wkt": "LINESTRING(45.123 78.901, 46.234 79.012)"},
    {"name": "Shyzhyn River", "wkt": "LINESTRING(47.345 80.123, 48.456 81.234)"}
]

# Добавление рек на карту
for river in river_coords:
    geom = wkt.loads(river["wkt"])
    folium.GeoJson(geom, style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)
    folium.Marker(geom.centroid, popup=river["name"], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты
m.save("154.html")