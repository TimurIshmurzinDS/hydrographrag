import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile в GeoPandas-объекте, преобразовав его в CRS 'EPSG:4326'
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту Folium с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(gdf.centroid.iloc[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте бассейн на карту как GeoJson
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создайте hardcoded список словарей с координатами в WKT-формате для реки Шыжын и Дос
river_coords = [
    {'name': 'Shyzhyn River', 'wkt': 'POINT(48.1234 77.5678)'},
    {'name': 'Byzhy River', 'wkt': 'POINT(49.2345 78.9012)'}
]

# Добавьте точки на карту
for river in river_coords:
    folium.Marker(folium.Location([river['wkt'].coords[1], river['wkt'].coords[0]]), 
                  popup=river['name']).add_to(m)

# Рассчитайте расстояние между началом реки Шыжын и точкой слияния
shyzhyn_start = wkt.loads(river_coords[0]['wkt'])
dos_merge_point = wkt.loads('POINT(48.1234 77.5678)') # hardcoded координаты точки слияния
distance = shyzhyn_start.distance(dos_merge_point)

# Добавьте текст с расстоянием на карту
folium.Marker(folium.Location([48.1234, 77.5678]), 
              popup=f'Расстояние до слияния: {distance:.2f} км').add_to(m)

# Сохраните карту в файл
m.save("104.html")