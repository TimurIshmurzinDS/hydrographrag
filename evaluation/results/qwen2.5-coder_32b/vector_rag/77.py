import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты folium
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример данных о координатах рек (WKT)
river_coordinates = [
    {"name": "Prokhodnaya River", "wkt": "LINESTRING(37.5 56.1, 38.0 56.2)"},
    {"name": "Baskan River", "wkt": "LINESTRING(39.0 55.9, 39.5 56.0)"}
]

# Добавление линий рек на карту
for river in river_coordinates:
    line = wkt.loads(river["wkt"])
    folium.PolyLine(locations=[[p.y, p.x] for p in line.coords], color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("77.html")