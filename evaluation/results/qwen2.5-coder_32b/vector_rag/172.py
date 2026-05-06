import geopandas as gpd
import folium
from shapely import wkt

# Загрузка границы бассейна и преобразование в EPSG:4326
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs(epsg=4326)

# Инициализация карты с использованием центроида полигона бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границы бассейна на карту
folium.GeoJson(basin.to_json(), name="Бассейн реки Текес", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть наблюдения в виде точек (WKT), хотя они не предоставлены в контексте
# Пример списка словарей с координатами наблюдений
observations = [
    {'name': 'с.Tekes_1', 'geometry': wkt.loads('POINT(80.2345 42.7654)')},
    {'name': 'с.Tekес_2', 'geometry': wkt.loads('POINT(80.3456 42.8765)')},
    {'name': 'с.Tekес_3', 'geometry': wkt.loads('POINT(80.4567 42.9876)')},
    {'name': 'с.Tекес_4', 'geometry': wkt.loads('POINT(80.5678 43.0987)')}
]

# Добавление наблюдений на карту
for obs in observations:
    folium.Marker([obs['geometry'].y, obs['geometry'].x], popup=obs['name']).add_to(m)

# Сохранение карты в файл
m.save("172.html")