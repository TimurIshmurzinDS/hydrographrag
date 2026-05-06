import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты рек (пример, если есть WKT)
rivers = [
    {"name": "Sharyn River", "geometry": wkt.loads("LINESTRING(79.85 43.15, 80.05 43.25)")},
    {"name": "Sarykan River", "geometry": wkt.loads("LINESTRING(79.90 43.20, 80.10 43.30)")},
    {"name": "Tokyraun River", "geometry": wkt.loads("LINESTRING(79.95 43.25, 80.15 43.35)")}
]

# Добавление рек на карту
for river in rivers:
    folium.GeoJson(river["geometry"], name=river["name"]).add_to(m)

# Сохранение карты в файл
m.save("194.html")