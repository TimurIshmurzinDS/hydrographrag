import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Пример координат (WKT), если они есть в контексте
coordinates = [
    {"name": "Lepsy River", "wkt": "LINESTRING(35.123 48.456, 35.789 48.123)"},
    {"name": "Dos River", "wkt": "LINESTRING(35.456 48.789, 36.123 48.456)"}
]

# Добавление линий рек на карту
for coord in coordinates:
    line = wkt.loads(coord["wkt"])
    folium.PolyLine(locations=[[p.y, p.x] for p in line.coords], color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты
m.save("128.html")