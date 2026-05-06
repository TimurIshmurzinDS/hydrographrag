import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек наблюдений (координаты должны быть предоставлены в формате WKT)
observations = [
    {"name": "Observation 1", "geometry": wkt.loads("POINT(75.3456 42.8901)")},  # Примерные координаты
    {"name": "Observation 2", "geometry": wkt.loads("POINT(75.3457 42.8902)")},  # Примерные координаты
    {"name": "Observation 3", "geometry": wkt.loads("POINT(75.3458 42.8903)")}   # Примерные координаты
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['geometry'].y, obs['geometry'].x],
        popup=obs["name"],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("73.html")