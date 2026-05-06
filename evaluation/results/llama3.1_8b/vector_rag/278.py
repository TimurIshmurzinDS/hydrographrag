import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с географической информацией о регионе
gdf = gpd.read_file(r"data/basin_data.shp").to_crs('EPSG:4326')

# Создание карты с центром в середине региона и параметрами tiles='CartoDB positron'
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление региона на карту
folium.GeoJson(gdf.to_json(), name='region').add_to(m)

# Создание списка словарей с координатами (WKT)
wkt_coords = [
    {'lat': 55.7558, 'lon': 37.6173},
    {'lat': 40.7128, 'lon': -74.0060},
    {'lat': 34.0522, 'lon': -118.2437}
]

# Добавление маркеров на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], popup='Маркер').add_to(m)

# Сохранение карты в файл
m.save("278.html")