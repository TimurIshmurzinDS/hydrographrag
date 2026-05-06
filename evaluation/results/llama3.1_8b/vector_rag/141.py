import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне в формате shapefile
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_data.to_json(), name='basin').add_to(m)

# Создание списка точек мониторинга с критическими уровнями воды
critical_points = [
    {'lat': 55.7558, 'lon': 37.6173, 'level': 10},
    {'lat': 40.7128, 'lon': -74.0060, 'level': 15},
    {'lat': 34.0522, 'lon': -118.2437, 'level': 20}
]

# Добавление точек мониторинга на карту
for point in critical_points:
    folium.Marker([point['lat'], point['lon']], popup=f'Уровень воды: {point["level"]} см').add_to(m)

# Сохранение карты в файл
m.save("141.html")