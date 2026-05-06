import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границей водного бассейна и преобразование в CRS 'EPSG:4326'
basin = gpd.read_file(r"data/basin_data.shp")
basin = basin.to_crs(epsg=4326)

# Инициализация карты с центром в центроиде водного бассейна
centroid = basin.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление границы водного бассейна на карту
folium.GeoJson(basin.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка словарей с координатами точек наблюдения (предполагается, что координаты не предоставлены в контексте)
# В реальном сценарии здесь должны быть добавлены фактические координаты
observation_points = [
    {'name': 'Observation 1', 'coordinates': wkt.loads('POINT(76.923077 42.865699)')},  # Примерные координаты
    {'name': 'Observation 2', 'coordinates': wkt.loads('POINT(76.923077 42.865699)')},
    {'name': 'Observation 3', 'coordinates': wkt.loads('POINT(76.923077 42.865699)')},
    {'name': 'Observation 4', 'coordinates': wkt.loads('POINT(76.923077 42.865699)')}
]

# Добавление точек наблюдения на карту
for point in observation_points:
    folium.Marker(
        location=[point['coordinates'].y, point['coordinates'].x],
        popup=point['name'],
        icon=folium.Icon(color='blue')
    ).add_to(m)

# Сохранение карты в файл
m.save("15.html")