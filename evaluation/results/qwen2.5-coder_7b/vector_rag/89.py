import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты наблюдений (пример)
observations = [
    {"name": "Prokhodnaya River", "wkt": "POINT(37.123456 55.678901)"},
    {"name": "Baskan River", "wkt": "POINT(37.234567 55.789012)"}
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(obs["wkt"])
    folium.Marker([point.y, point.x], popup=obs["name"]).add_to(m)

# Сохранение карты
m.save("89.html")