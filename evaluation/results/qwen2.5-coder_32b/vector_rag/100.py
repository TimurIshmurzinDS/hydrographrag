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
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположительные координаты рек в формате WKT (пример)
river_coordinates = [
    {"name": "Shyzhyn River", "wkt": "LINESTRING(75.34 49.86, 75.35 49.87)"},
    {"name": "Byzhy River", "wkt": "LINESTRING(75.35 49.87, 75.36 49.88)"},
    {"name": "Shynzhaly River", "wkt": "LINESTRING(75.36 49.88, 75.37 49.89)"},
    {"name": "Prokhodnaya River", "wkt": "LINESTRING(75.37 49.89, 75.38 49.90)"}
]

# Добавление рек на карту
for river in river_coordinates:
    line = wkt.loads(river["wkt"])
    folium.PolyLine(locations=[[p.y, p.x] for p in line.coords], color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("100.html")