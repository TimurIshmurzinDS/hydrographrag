import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными бассейна
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты Folium с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка точек на реке Кishi Osek
points = [
    {'lat': 55.123456, 'lon': 37.654321},
    {'lat': 55.234567, 'lon': 38.765432},
    {'lat': 55.345678, 'lon': 39.876543}
]

# Добавление точек на карту
for point in points:
    folium.Marker(point['lat'], point['lon']).add_to(m)

# Сохранение карты в файл
m.save("261.html")