import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.to_json(), name='bass').add_to(m)

# Создание списка точек с координатами (WKT)
points = [
    {'name': 'Река Бызж', 'geometry': wkt.loads('POINT(48.123 77.456)')},
    {'name': 'Река Шижин', 'geometry': wkt.loads('POINT(49.789 78.321)')},
    {'name': 'Река Уржар', 'geometry': wkt.loads('POINT(47.654 76.987)')}
]

# Добавление точек на карту
for point in points:
    folium.Marker(location=[point['geometry'].coords[1], point['geometry'].coords[0]], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("185.html")