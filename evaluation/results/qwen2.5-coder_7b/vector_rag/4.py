import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с границами бассейна
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data = basin_data.to_crs('EPSG:4326')

# Создание карты с центром в centroid бассейна
centroid = basin_data.geometry.centroid[0]
m = folium.Map(location=[centroid.y, centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавление границ бассейна на карту
folium.GeoJson(basin_data.to_json(), style_function=lambda x: {
    'fillColor': 'green',
    'color': 'darkgreen',
    'fillOpacity': 0.2
}).add_to(m)

# Пример координат станции мониторинга на реке Koktal River (WKT)
monitoring_station_coords = [
    {'name': 'Station1', 'wkt': 'POINT(43.5678 49.1234)'},
    {'name': 'Station2', 'wkt': 'POINT(43.6789 49.2345)'}
]

# Добавление станций мониторинга на карту
for station in monitoring_station_coords:
    point = wkt.loads(station['wkt'])
    folium.Marker([point.y, point.x], popup=station['name'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("4.html")