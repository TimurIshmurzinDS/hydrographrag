import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=[basin_data.centroid.y, basin_data.centroid.x], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(data=basin_data.to_json(), name='basin').add_to(m)

# Создать список точек с данными о стоке реки (в данном случае hardcoded)
points = [
    {'location': [40.1234, 45.6789], 'value': 100},
    {'location': [40.2345, 46.7890], 'value': 200},
    {'location': [40.3456, 47.8901], 'value': 300}
]

# Добавить точки на карту
for point in points:
    folium.Marker(point['location'], popup=str(point['value'])).add_to(m)

# Сохранить карту в файл
m.save("192.html")