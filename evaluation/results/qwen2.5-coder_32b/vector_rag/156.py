import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Или
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Получение центроида для инициализации карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=8)

# Добавление бассейна реки Или на карту
folium.GeoJson(basin_data, style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты притоков (примерные данные)
river_coordinates = [
    {"name": "Sarykan River", "wkt": "LINESTRING(76.85 43.15, 77.05 43.25)"},
    {"name": "Shynzhaly River", "wkt": "LINESTRING(79.25 42.85, 79.45 42.95)"}
]

# Добавление притоков на карту
for river in river_coordinates:
    geom = wkt.loads(river["wkt"])
    folium.PolyLine(locations=list(geom.coords), color='blue', weight=2.5, opacity=1).add_to(m)

# Сохранение карты в файл
m.save("156.html")