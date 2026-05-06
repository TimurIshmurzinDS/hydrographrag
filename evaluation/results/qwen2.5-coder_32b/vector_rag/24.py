import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне реки Улкен Алматы
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с использованием центроида полигона бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление полигона бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами точек наблюдений
# Предполагается, что координаты точек не предоставлены в контексте, поэтому создаем примерные координаты
observation_points = [
    {'name': 'Observation 1', 'coordinates': (centroid.y + 0.001, centroid.x)},
    {'name': 'Observation 2', 'coordinates': (centroid.y - 0.001, centroid.x)},
    {'name': 'Observation 3', 'coordinates': (centroid.y, centroid.x + 0.001)},
    {'name': 'Observation 4', 'coordinates': (centroid.y, centroid.x - 0.001)}
]

# Добавление маркеров на карту
for point in observation_points:
    folium.Marker(location=point['coordinates'], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("24.html")