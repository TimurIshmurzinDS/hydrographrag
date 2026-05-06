import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
basin_data = gpd.read_file(r"data/basin_data.shp")
basin_data.crs = 'EPSG:4326'

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=basin_data.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(data=basin_data.to_crs(epsg=3857).geometry.apply(lambda x: x.__geo_interface__)).add_to(m)

# Создание списка точек наблюдений (в данном случае hardcoded)
points = [
    {'lat': 43.123456, 'lon': 76.789012},
    {'lat': 43.234567, 'lon': 77.890123},
    {'lat': 43.345678, 'lon': 78.901234},
    {'lat': 43.456789, 'lon': 79.012345}
]

# Добавление точек на карту
for point in points:
    folium.Marker(location=[point['lat'], point['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("217.html")