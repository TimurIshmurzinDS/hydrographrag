import geopandas as gpd
import folium
from shapely import wkt

# Загрузить данные о бассейнах рек из файла data/basin_data.shp
basins_gdf = gpd.read_file(r"data\bassin_data.shp")
basins_gdf = basins_gdf.to_crs('EPSG:4326')

# Создать карту с использованием библиотеки Folium
m = folium.Map(location=basins_gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(data=basins_gdf.to_json(), name='basins').add_to(m)

# Создать список словарей для представления координат села Темирлик
temirlik_village_coords = [
    {'lat': 43.1234, 'lon': 79.5678},
    {'lat': 43.2345, 'lon': 79.6789},
    {'lat': 43.3456, 'lon': 79.7890}
]

# Нарисовать на карте точки наблюдений села Темирлик
for coord in temirlik_village_coords:
    folium.Marker(location=[coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранить карту в файл
m.save("115.html")