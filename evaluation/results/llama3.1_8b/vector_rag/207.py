import geopandas as gpd
from shapely import wkt

# Загрузить shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создать карту Folium с центром в середине бассейна и использованием плиток CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту как GeoJSON
folium.GeoJson(gdf.to_crs('EPSG:4326').geometry.__geo_interface__, 
               name='basin',
               style={'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создать список словарей для точек наблюдения
points = [
    {'name': 'Пункт наблюдения 1', 'location': wkt.loads('POINT(78.1234 46.5678)')},
    {'name': 'Пункт наблюдения 2', 'location': wkt.loads('POINT(79.2345 47.6789)')},
    {'name': 'Пункт наблюдения 3', 'location': wkt.loads('POINT(80.3456 48.7890)')}
]

# Добавить точки наблюдения на карту
for point in points:
    folium.Marker(point['location'], popup=point['name']).add_to(m)

# Сохранить карту в файл
m.save("207.html")