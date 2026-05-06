import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты рек (пример, если есть WKT данные)
river_coordinates = [
    {"name": "Emel River", "wkt": "LINESTRING(75.9346 41.8820, 76.0346 41.9820)"},
    {"name": "Turgen River", "wkt": "LINESTRING(76.1346 42.0820, 76.2346 42.1820)"}
]

# Добавление рек на карту
for river in river_coordinates:
    line = wkt.loads(river["wkt"])
    folium.PolyLine(locations=[[p.y, p.x] for p in line.coords], color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("202.html")