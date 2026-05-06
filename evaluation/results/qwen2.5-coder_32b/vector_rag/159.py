import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs(epsg=4326)

# Инициализация карты с центроидом бассейна
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Если доступны координаты точек наблюдений (WKT), добавить их на карту
# Пример списка словарей с координатами и описанием
observations = [
    {'wkt': 'POINT(76.93 42.85)', 'description': 'Observation_2284'},
    {'wkt': '77.01 42.90', 'description': 'Observation_2219'}
]

# Добавление маркеров на карту
for obs in observations:
    point = wkt.loads(obs['wkt'])
    folium.Marker([point.y, point.x], popup=obs['description']).add_to(m)

# Сохранение карты в файл
m.save("159.html")