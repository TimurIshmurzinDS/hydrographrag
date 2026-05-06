import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Создание карты
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление области бассейна на карту
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: x.wkt),
               name='basin',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек с координатами (WKT)
points = [
    {'name': 'Точка 1', 'geometry': wkt.loads('POINT(76.5 43.5)')},
    {'name': 'Точка 2', 'geometry': wkt.loads('POINT(77.0 44.0)')}
]

# Добавление точек на карту
for point in points:
    folium.Marker(point['geometry'].coords[0], popup=point['name']).add_to(m)

# Сохранение карты в файл
m.save("256.html")