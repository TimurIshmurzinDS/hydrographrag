import geopandas as gpd
import folium
from shapely import wkt

# Загрузить shapefile с внешними границами бассейна
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создать карту с центром в середине бассейна и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавить бассейн на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создать список точек в виде словарей
points = [
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.234567, 'lon': 77.890123}
]

# Добавить точки на карту
for point in points:
    folium.Marker(point).add_to(m)

# Сохранить карту в файл
m.save("102.html")