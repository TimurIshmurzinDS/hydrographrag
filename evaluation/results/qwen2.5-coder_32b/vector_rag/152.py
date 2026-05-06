import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты рек (примерные, для демонстрации)
rivers = [
    {"name": "Lepsy River", "geometry": wkt.loads("LINESTRING(69.15 43.85, 69.20 43.90)")},
    {"name": "Shilik River", "geometry": wkt.loads("LINESTRING(69.25 43.95, 69.30 44.00)")}
]

# Добавление рек на карту
for river in rivers:
    folium.GeoJson(river["geometry"], name=river["name"]).add_to(m)

# Сохранение карты в файл
m.save("152.html")