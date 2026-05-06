import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна (только для контекста)
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=8, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты для Tentek River и Sharyn River (примерные)
tentek_coords = [
    {"name": "Tentek River", "wkt": "LINESTRING(76.9531 43.2283, 76.9531 43.2283)"}
]

sharyn_coords = [
    {"name": "Sharyn River", "wkt": "LINESTRING(76.0000 43.0000, 76.0000 43.0000)"}
]

# Добавление рек на карту
for river in tentek_coords:
    geom = wkt.loads(river["wkt"])
    folium.GeoJson(geom, style_function=lambda x: {'color': 'blue', 'weight': 2}).add_to(m)

for river in sharyn_coords:
    geom = wkt.loads(river["wkt"])
    folium.GeoJson(geom, style_function=lambda x: {'color': 'red', 'weight': 2}).add_to(m)

# Сохранение карты
m.save("75.html")