import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о реке Киши Осек
basin_data = r"data/basin_data.shp"
gdf = gpd.read_file(basin_data)
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в centroid базина
centroid = gdf.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=12, tiles='CartoDB positron')

# Добавление базина на карту
folium.GeoJson(gdf.to_json(), style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Координаты наблюдений (пример)
observations = [
    {"name": "Observation 1", "wkt": "POINT(37.5648 55.7558)"},
    {"name": "Observation 2", "wkt": "POINT(37.5650 55.7560)"},
    {"name": "Observation 3", "wkt": "POINT(37.5652 55.7562)"}
]

# Добавление точек наблюдений на карту
for obs in observations:
    point = wkt.loads(obs["wkt"])
    folium.Marker([point.y, point.x], popup=obs["name"]).add_to(m)

# Сохранение карты в файл
m.save("261.html")