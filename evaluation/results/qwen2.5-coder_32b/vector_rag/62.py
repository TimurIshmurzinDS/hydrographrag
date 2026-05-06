import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Инициализация карты с центром в бассейне реки Шарын
centroid = basin_data.geometry.centroid.iloc[0]
m = folium.Map(location=[centroid.y, centroid.x], tiles='CartoDB positron', zoom_start=10)

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), name="Basin", style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Предположим, что у нас есть данные о постах мониторинга в формате WKT и их статусе
monitoring_stations = [
    {'name': 'Station1', 'geometry': wkt.loads('POINT(79.85 42.30)'), 'status': 'active'},
    {'name': 'Station2', 'geometry': wkt.loads('POINT(79.90 42.35)'), 'status': 'inactive'},
    {'name': 'Station3', 'geometry': wkt.loads('POINT(80.00 42.40)'), 'status': 'active'}
]

# Добавление постов мониторинга на карту
for station in monitoring_stations:
    if station['status'] == 'inactive':
        folium.Marker(
            location=[station['geometry'].y, station['geometry'].x],
            popup=station['name'],
            icon=folium.Icon(color='red', icon='info-sign')
        ).add_to(m)

# Сохранение карты в файл
m.save("62.html")