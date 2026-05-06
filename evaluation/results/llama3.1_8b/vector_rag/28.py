import geopandas as gpd
import folium
from shapely import wkt

# Загрузка shapefile с данными о бассейне
gdf = gpd.read_file(r"data/basin_data.shp")
gdf = gdf.to_crs('EPSG:4326')

# Создание карты с центром в середине бассейна и использованием слоя CartoDB positron
m = folium.Map(location=gdf.centroid.coords[0], zoom_start=10, tiles='CartoDB positron')

# Добавление бассейна на карту
folium.GeoJson(gdf.to_json(), name='basin').add_to(m)

# Создание списка словарей для координат WKT (если они есть)
wkt_coords = [
    {'lat': 43.1234, 'lon': 45.6789},
    {'lat': 43.2345, 'lon': 46.7890}
]

# Добавление точек на карту
for coord in wkt_coords:
    folium.Marker([coord['lat'], coord['lon']], icon=folium.Icon(color='red')).add_to(m)

# Сохранение карты в файл
m.save("28.html")