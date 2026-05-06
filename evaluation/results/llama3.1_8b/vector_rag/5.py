import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне из shapefile в формате EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту в виде GeoJson с зеленой заливкой
folium.GeoJson(data=basin_data.to_json(), name='бассейн').add_child(
    folium.features.GeoJsonTooltip(fields=['name'], aliases=['Имя'], labels=True)
).add_to(m)

# Создание списка точек наблюдения в виде hardcoded-список словарей
observation_points = [
    {'location': wkt.loads('POINT(55.123 37.456)'), 'level': None},
    {'location': wkt.loads('POINT(55.124 37.457)'), 'level': None},
    {'location': wkt.loads('POINT(55.125 37.458)'), 'level': None},
    {'location': wkt.loads('POINT(55.126 37.459)'), 'level': None}
]

# Добавление точек наблюдения на карту
for point in observation_points:
    folium.Marker(point['location'], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл с именем "5.html"
m.save("5.html")