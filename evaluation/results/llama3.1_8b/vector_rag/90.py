import geopandas as gpd
import folium
from shapely import wkt

# Загрузите shapefile с использованием raw string и преобразуйте его в CRS 'EPSG:4326'
basin_gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создайте карту с центром в середине области
m = folium.Map(location=basin_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавьте область на карту с использованием GeoJson
folium.GeoJson(data=basin_gdf.to_json(), name='basin').add_to(m)

# Создайте список рек в виде словарей (поскольку координаты отсутствуют, они будут hardcoded)
rivers = [
    {'name': 'Karaoy River', 'geometry': wkt.loads('POINT(0 0)')},
    {'name': 'Baskan River', 'geometry': wkt.loads('POINT(1 1)')},
    {'name': 'Temirlik River', 'geometry': wkt.loads('POINT(2 2)')}
]

# Добавьте реки на карту
for river in rivers:
    folium.Marker(location=river['geometry'].coords[0], popup=river['name']).add_to(m)

# Сохраните карту в файле HTML
m.save("90.html")