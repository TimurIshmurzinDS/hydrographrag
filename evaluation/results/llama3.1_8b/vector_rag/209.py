import geopandas as gpd
import folium
from shapely import wkt

# Загрузка данных о бассейне
basin_gdf = gpd.read_file(r"data/basin_data.shp")
basin_gdf.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(basin_gdf.to_crs(epsg=3857).geometry.apply(lambda x: wkt.dumps(x)).tolist(),
               name='Бассейн реки Уржар',
               style_function=lambda x: {'fillColor': 'green', 'color': 'darkgreen', 'fillOpacity': 0.2}).add_to(m)

# Создание списка точек с координатами (WKT)
points = [
    {'location': wkt.loads('POINT(48.6784 82.9833)')},
    {'location': wkt.loads('POINT(48.6791 83.0123)')}
]

# Добавление точек на карту
for point in points:
    folium.Marker(point['location'].coords[0], popup='Точка').add_to(m)

# Сохранение карты в файл
m.save("209.html")