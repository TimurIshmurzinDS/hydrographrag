import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных бассейна реки
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей для точек наблюдений (предполагается, что координаты отсутствуют в контексте)
observations = [
    {'name': 'Observation 1', 'coordinates': wkt.loads('POINT(37.620405 55.755826)')},  # Примерные координаты
    {'name': 'Observation 2', 'coordinates': wkt.loads('POINT(37.619405 55.754826)')},
    {'name': 'Observation 3', 'coordinates': wkt.loads('POINT(37.618405 55.753826)')},
    {'name': 'Observation 4', 'coordinates': wkt.loads('POINT(37.617405 55.752826)')}
]

# Добавление точек наблюдений на карту
for obs in observations:
    folium.Marker(
        location=[obs['coordinates'].y, obs['coordinates'].x],
        popup=obs['name'],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("12.html")