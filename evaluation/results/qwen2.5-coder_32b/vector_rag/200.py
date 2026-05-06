import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=12)

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предполагаемые координаты точки наблюдения (1.7 км выше устья реки Kishi Osek)
# В данном примере используются произвольные координаты для демонстрации
observation_points = [
    {'name': 'Observation Point 1', 'coordinates': wkt.loads('POINT(38.25 40.75)')},
    {'name': 'Observation Point 2', 'coordinates': wkt.loads('POINT(38.26 40.76)')},
    {'name': 'Observation Point 3', 'coordinates': wkt.loads('POINT(38.27 40.77)')}
]

# Добавление точек наблюдения на карту
for point in observation_points:
    folium.Marker(
        location=[point['coordinates'].y, point['coordinates'].x],
        popup=point['name'],
        icon=folium.Icon(color='red')
    ).add_to(m)

# Сохранение карты в файл
m.save("200.html")