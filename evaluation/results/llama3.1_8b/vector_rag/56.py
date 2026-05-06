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

# Создать список словарей для точек измерения водного уровня
points = [
    {'lat': 55.123, 'lon': 36.456, 'value': 10},
    {'lat': 55.234, 'lon': 37.567, 'value': 20},
    {'lat': 55.345, 'lon': 38.678, 'value': 30}
]

# Добавить точки на карту
for point in points:
    folium.Marker([point['lat'], point['lon']], popup=f'Водный уровень: {point["value"]}').add_to(m)

# Сохранить карту в файл
m.save("56.html")