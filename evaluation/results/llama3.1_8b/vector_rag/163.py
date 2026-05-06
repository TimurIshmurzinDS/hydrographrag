import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с данными бассейна в системе координат EPSG:4326
basin_data = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=basin_data.centroid, zoom_start=10, tiles='CartoDB positron')

# Добавить данные бассейна на карту
folium.GeoJson(data=basin_data.unary_union.__geo_interface__, name='Basin').add_to(m)

# Создать список точек (WKT) для рек в системе координат EPSG:4326
points = [
    {'type': 'Feature', 'geometry': wkt.loads('POINT(48.1234 77.5678)'), 'properties': {'name': 'Shyzhyn River'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(49.2345 78.9012)'), 'properties': {'name': 'Sarykan River'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(47.6789 76.3456)'), 'properties': {'name': 'Shynzhaly River'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(48.9012 77.5678)'), 'properties': {'name': 'Byzhy River'}},
    {'type': 'Feature', 'geometry': wkt.loads('POINT(49.2345 78.9012)'), 'properties': {'name': 'Sharyn River'}}
]

# Добавить точки на карту
folium.FeatureGroup(name='Реки').add_child(folium.Marker(location=[point['geometry']['coordinates'][1], point['geometry']['coordinates'][0]], popup=point['properties']['name']).add_to(m) for point in points)

# Сохранить карту в файл html
m.save("163.html")